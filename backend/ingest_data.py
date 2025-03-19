import os
import json
import logging
import time
from datetime import datetime, timedelta
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
from app import app, db, Event
from dotenv import load_dotenv

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# File to store checkpoint data
CHECKPOINT_FILE = os.path.join(os.path.dirname(__file__), 'checkpoint.json')

# Category normalization mapping (if needed)
CATEGORY_MAPPING = {
    "Music": "Concert",
    "Sports": "Game",
    "Arts & Theatre": "Performance"
}

class EventIngestionService:
    def __init__(self):
        load_dotenv()  # Ensure environment variables are loaded
        self.ticketmaster_api_key = os.environ.get("TICKETMASTER_API_KEY")
        if not self.ticketmaster_api_key:
            raise ValueError("TICKETMASTER_API_KEY is required in .env file")
        self.eventbrite_api_key = os.environ.get("EVENTBRITE_API_KEY")
        if not self.eventbrite_api_key:
            raise ValueError("EVENTBRITE_API_KEY is required in .env file")
        # Google Places API key is optional; if not provided, we skip that integration.
        self.google_places_api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
        
        self.ticketmaster_base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
        # Remove trailing slash to avoid 404 issues
        self.eventbrite_base_url = "https://www.eventbriteapi.com/v3/events/search"
        self.checkpoint_file = CHECKPOINT_FILE

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch_ticketmaster_events(self, page: int, start_date: datetime, end_date: datetime):
        params = {
            'apikey': self.ticketmaster_api_key,
            'city': 'Las Vegas',
            'stateCode': 'NV',
            'size': 100,
            'page': page,
            'sort': 'date,asc',
            'startDateTime': start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'endDateTime': end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        logger.info(f"Ticketmaster: Requesting {self.ticketmaster_base_url} with params: {params}")
        response = requests.get(self.ticketmaster_base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch_eventbrite_events(self, page: int, start_date: datetime, end_date: datetime):
        headers = {"Authorization": f"Bearer {self.eventbrite_api_key}"}
        params = {
            "location.address": "Las Vegas",
            "sort_by": "date",
            "page": page,
            "start_date.range_start": start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "start_date.range_end": end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        logger.info(f"Eventbrite: Requesting {self.eventbrite_base_url} with params: {params}")
        response = requests.get(self.eventbrite_base_url, headers=headers, params=params, timeout=10)
        try:
            response.raise_for_status()
        except requests.HTTPError as he:
            logger.error(f"Eventbrite HTTPError: {he}, Response: {response.text}")
            raise he
        data = response.json()
        logger.info(f"Eventbrite: Received response: {json.dumps(data)[:500]}...")
        return data

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch_google_places_events(self, next_page_token=None):
        if not self.google_places_api_key:
            logger.info("No Google Places API key provided; skipping Google Places ingestion.")
            return None
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": "events in Las Vegas",
            "key": self.google_places_api_key
        }
        if next_page_token:
            params["pagetoken"] = next_page_token
        logger.info(f"Google Places: Requesting {base_url} with params: {params}")
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Google Places: Received response: {json.dumps(data)[:500]}...")
        return data

    def process_ticketmaster_event(self, event_data: dict):
        try:
            external_id = event_data.get("id")
            name = event_data.get("name")
            description = event_data.get("description", "")
            start_date_str = event_data.get("dates", {}).get("start", {}).get("dateTime", "")
            if start_date_str:
                try:
                    parsed_start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                except Exception as parse_error:
                    logger.error(f"Error parsing start date for Ticketmaster event {external_id}: {parse_error}")
                    parsed_start_date = None
            else:
                parsed_start_date = None
            venue = None
            latitude = None
            longitude = None
            address = None
            if event_data.get("_embedded", {}).get("venues"):
                venue_data = event_data["_embedded"]["venues"][0]
                venue = venue_data.get("name")
                if venue_data.get("location"):
                    latitude = float(venue_data["location"].get("latitude", 0))
                    longitude = float(venue_data["location"].get("longitude", 0))
                if venue_data.get("address"):
                    address_parts = []
                    if venue_data["address"].get("line1"):
                        address_parts.append(venue_data["address"]["line1"])
                    if venue_data.get("city", {}).get("name"):
                        address_parts.append(venue_data["city"]["name"])
                    if venue_data.get("state", {}).get("stateCode"):
                        address_parts.append(venue_data["state"]["stateCode"])
                    if venue_data.get("postalCode"):
                        address_parts.append(venue_data["postalCode"])
                    address = ", ".join(address_parts)

            # Get price range
            price_range_min = None
            price_range_max = None
            if event_data.get("priceRanges"):
                price_range = event_data["priceRanges"][0]
                price_range_min = price_range.get("min")
                price_range_max = price_range.get("max")

            # Get image URL
            image_url = None
            if event_data.get("images"):
                # Try to get the largest image
                images = sorted(event_data["images"], key=lambda x: x.get("width", 0), reverse=True)
                if images:
                    image_url = images[0].get("url")

            # Get tags/keywords
            tags = []
            if event_data.get("classifications"):
                classification = event_data["classifications"][0]
                for field in ["segment", "genre", "subGenre"]:
                    if classification.get(field, {}).get("name") and classification[field]["name"].lower() != "undefined":
                        tags.append(classification[field]["name"].lower())

            # Get rating and review count (if available in raw data)
            rating = None
            review_count = None
            if event_data.get("_embedded", {}).get("venues"):
                venue_data = event_data["_embedded"]["venues"][0]
                if venue_data.get("generalInfo"):
                    rating = venue_data["generalInfo"].get("rating")
                    review_count = venue_data["generalInfo"].get("reviewCount")

            processed = {
                'external_id': external_id,
                'name': name,
                'description': description,
                'category': event_data.get("classifications", [{}])[0].get("segment", {}).get("name"),
                'subcategory': event_data.get("classifications", [{}])[0].get("genre", {}).get("name"),
                'price_range_min': price_range_min,
                'price_range_max': price_range_max,
                'venue': venue,
                'start_date': parsed_start_date,
                'end_date': None,  # Ticketmaster doesn't always provide end dates
                'image_url': image_url,
                'source': 'ticketmaster',
                'latitude': latitude,
                'longitude': longitude,
                'address': address,
                'tags': tags,
                'url': event_data.get("url"),
                'rating': rating,
                'review_count': review_count
            }
            logger.info(f"Ticketmaster event processed: {external_id}, start: {parsed_start_date}")
            return processed
        except Exception as e:
            logger.error(f"Error processing Ticketmaster event {event_data.get('id')}: {e}")
            return None

    def process_eventbrite_event(self, event_data: dict):
        try:
            external_id = event_data.get("id")
            name = event_data.get("name", {}).get("text")
            description = event_data.get("description", {}).get("text", "")
            start_date_str = event_data.get("start", {}).get("local", "")
            if start_date_str:
                try:
                    parsed_start_date = datetime.fromisoformat(start_date_str)
                except Exception as parse_error:
                    logger.error(f"Error parsing start date for Eventbrite event {external_id}: {parse_error}")
                    parsed_start_date = None
            else:
                parsed_start_date = None

            # Get venue and location information
            venue = None
            latitude = None
            longitude = None
            address = None
            if event_data.get("venue"):
                venue_data = event_data["venue"]
                venue = venue_data.get("name")
                if venue_data.get("latitude") and venue_data.get("longitude"):
                    latitude = float(venue_data["latitude"])
                    longitude = float(venue_data["longitude"])
                address_parts = []
                if venue_data.get("address", {}).get("address_1"):
                    address_parts.append(venue_data["address"]["address_1"])
                if venue_data.get("address", {}).get("city"):
                    address_parts.append(venue_data["address"]["city"])
                if venue_data.get("address", {}).get("region"):
                    address_parts.append(venue_data["address"]["region"])
                if venue_data.get("address", {}).get("postal_code"):
                    address_parts.append(venue_data["address"]["postal_code"])
                if address_parts:
                    address = ", ".join(address_parts)

            # Get image URL
            image_url = None
            if event_data.get("logo"):
                image_url = event_data["logo"].get("url")

            # Get tags/categories
            tags = []
            if event_data.get("category"):
                tags.append(event_data["category"].get("name", "").lower())
            if event_data.get("subcategory"):
                tags.append(event_data["subcategory"].get("name", "").lower())
            if event_data.get("format"):
                tags.append(event_data["format"].get("name", "").lower())

            processed = {
                'external_id': external_id,
                'name': name,
                'description': description,
                'category': event_data.get("category", {}).get("name", "Event"),
                'subcategory': event_data.get("subcategory", {}).get("name"),
                'price_range_min': None,  # Eventbrite pricing requires additional API calls
                'price_range_max': None,
                'venue': venue,
                'start_date': parsed_start_date,
                'end_date': None,
                'image_url': image_url,
                'source': 'eventbrite',
                'latitude': latitude,
                'longitude': longitude,
                'address': address,
                'tags': tags,
                'url': event_data.get("url"),
                'rating': None,  # Eventbrite doesn't provide ratings
                'review_count': None
            }
            logger.info(f"Eventbrite event processed: {external_id}, start: {parsed_start_date}")
            return processed
        except Exception as e:
            logger.error(f"Error processing Eventbrite event {event_data.get('id')}: {e}")
            return None

    def process_google_places_event(self, place_data: dict):
        try:
            # Get basic place information
            external_id = place_data.get("place_id")
            name = place_data.get("name")
            
            # Get location information
            latitude = None
            longitude = None
            if place_data.get("geometry", {}).get("location"):
                latitude = place_data["geometry"]["location"].get("lat")
                longitude = place_data["geometry"]["location"].get("lng")

            # Get address
            address = place_data.get("formatted_address")

            # Get rating and review information
            rating = place_data.get("rating")
            review_count = place_data.get("user_ratings_total")

            # Get photos
            image_url = None
            if place_data.get("photos"):
                photo_reference = place_data["photos"][0].get("photo_reference")
                if photo_reference and self.google_places_api_key:
                    image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={photo_reference}&key={self.google_places_api_key}"

            # Get types as tags
            tags = place_data.get("types", [])

            processed = {
                'external_id': external_id,
                'name': name,
                'description': place_data.get("editorial_summary", {}).get("overview", ""),
                'category': "Google Places Event",
                'subcategory': None,
                'price_range_min': None,
                'price_range_max': None,
                'venue': name,
                'start_date': None,  # Google Places doesn't provide event dates
                'end_date': None,
                'image_url': image_url,
                'source': 'google_places',
                'latitude': latitude,
                'longitude': longitude,
                'address': address,
                'tags': tags,
                'url': place_data.get("url"),
                'rating': rating,
                'review_count': review_count
            }
            logger.info(f"Google Places event processed: {external_id}")
            return processed
        except Exception as e:
            logger.error(f"Error processing Google Places event {place_data.get('place_id')}: {e}")
            return None

    def ingest_data(self):
        with app.app_context():
            try:
                logger.info("Starting event ingestion process")
                now = datetime.utcnow()
                try:
                    with open(self.checkpoint_file, 'r') as f:
                        checkpoint = json.load(f)
                    start_date = datetime.strptime(
                        checkpoint.get('new_start_date', now.strftime('%Y-%m-%dT%H:%M:%SZ')),
                        '%Y-%m-%dT%H:%M:%SZ'
                    )
                    logger.info(f"Loaded checkpoint: {start_date}")
                except Exception as e:
                    start_date = now
                    logger.info("No valid checkpoint found; using current time as start_date.")
                end_of_year = datetime(now.year, 12, 31, 23, 59, 59)
                logger.info(f"Starting ingestion from {start_date} until {end_of_year}")
                overall_max_event_date = start_date
                total_processed = 0

                # --- Ticketmaster Ingestion ---
                page = 0
                while True:
                    logger.info(f"Ticketmaster: Fetching page {page} with startDateTime={start_date} and endDateTime={end_of_year}")
                    try:
                        tm_response = self.fetch_ticketmaster_events(page=page, start_date=start_date, end_date=end_of_year)
                    except RetryError as re:
                        logger.info(f"Ticketmaster: No more events available (error on page {page}). Breaking loop.")
                        break
                    if not tm_response or '_embedded' not in tm_response:
                        logger.info(f"Ticketmaster: No more data returned on page {page}.")
                        break
                    tm_events = tm_response['_embedded'].get('events', [])
                    if not tm_events:
                        logger.info(f"Ticketmaster: No events on page {page}.")
                        break
                    logger.info(f"Ticketmaster: Fetched {len(tm_events)} events on page {page}")
                    for event_data in tm_events:
                        processed_event = self.process_ticketmaster_event(event_data)
                        if not processed_event:
                            continue
                        event_start = processed_event.get('start_date')
                        if event_start:
                            event_start_naive = event_start.replace(tzinfo=None)
                            if event_start_naive > overall_max_event_date:
                                overall_max_event_date = event_start_naive
                        event = Event.query.filter_by(external_id=processed_event['external_id']).first()
                        if event:
                            for key, value in processed_event.items():
                                setattr(event, key, value)
                        else:
                            event = Event(**processed_event)
                            db.session.add(event)
                        total_processed += 1
                    db.session.commit()
                    logger.info(f"Ticketmaster: Processed {len(tm_events)} events on page {page}")
                    page += 1

                # --- Eventbrite Ingestion ---
                page = 1
                while True:
                    logger.info(f"Eventbrite: Fetching page {page} with start_date.range_start={start_date} and start_date.range_end={end_of_year}")
                    try:
                        eb_response = self.fetch_eventbrite_events(page=page, start_date=start_date, end_date=end_of_year)
                    except RetryError as re:
                        logger.info(f"Eventbrite: No more events available (error on page {page}). Breaking loop.")
                        break
                    eb_events = eb_response.get("events", [])
                    if not eb_events:
                        logger.info(f"Eventbrite: No events on page {page}.")
                        break
                    logger.info(f"Eventbrite: Fetched {len(eb_events)} events on page {page}")
                    for event_data in eb_events:
                        processed_event = self.process_eventbrite_event(event_data)
                        if not processed_event:
                            continue
                        event_start = processed_event.get("start_date")
                        if event_start:
                            event_start_naive = event_start.replace(tzinfo=None)
                            if event_start_naive > overall_max_event_date:
                                overall_max_event_date = event_start_naive
                        event = Event.query.filter_by(external_id=processed_event["external_id"]).first()
                        if event:
                            for key, value in processed_event.items():
                                setattr(event, key, value)
                        else:
                            event = Event(**processed_event)
                            db.session.add(event)
                        total_processed += 1
                    db.session.commit()
                    logger.info(f"Eventbrite: Processed {len(eb_events)} events on page {page}")
                    page += 1

                # --- Google Places Ingestion (Optional) ---
                if self.google_places_api_key:
                    next_page_token = None
                    while True:
                        try:
                            gp_response = self.fetch_google_places_events(next_page_token)
                        except RetryError as re:
                            logger.info("Google Places: No more events available (error retrieving page). Breaking loop.")
                            break
                        if not gp_response:
                            break
                        gp_events = gp_response.get("results", [])
                        if not gp_events:
                            logger.info("Google Places: No events found.")
                            break
                        logger.info(f"Google Places: Fetched {len(gp_events)} events")
                        for event_data in gp_events:
                            processed_event = self.process_google_places_event(event_data)
                            if not processed_event:
                                continue
                            event = Event.query.filter_by(external_id=processed_event["external_id"]).first()
                            if event:
                                for key, value in processed_event.items():
                                    setattr(event, key, value)
                            else:
                                event = Event(**processed_event)
                                db.session.add(event)
                            total_processed += 1
                        db.session.commit()
                        next_page_token = gp_response.get("next_page_token")
                        if not next_page_token:
                            break
                        logger.info("Google Places: Waiting for next_page_token to become valid...")
                        time.sleep(2)
                
                logger.info(f"✅ Successfully processed a total of {total_processed} events")
                logger.info(f"Latest event start date found: {overall_max_event_date}")
                new_checkpoint = {'new_start_date': overall_max_event_date.strftime('%Y-%m-%dT%H:%M:%SZ')}
                with open(self.checkpoint_file, 'w') as f:
                    json.dump(new_checkpoint, f)
                logger.info(f"Checkpoint saved: {new_checkpoint}")
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error during ingestion: {e}")
                raise e

def main():
    service = EventIngestionService()
    service.ingest_data()

if __name__ == "__main__":
    main()