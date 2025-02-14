import os
import requests
from datetime import datetime, timedelta
import logging
from app import app, db, Event, Recommendation
from dotenv import load_dotenv

load_dotenv()

# Category normalization mapping
CATEGORY_MAPPING = {
    "Music": "Concert",
    "Sports": "Game",
    "Arts & Theatre": "Performance"
}

class EventIngestionService:
    def __init__(self):
        self.api_key = os.environ.get("TICKETMASTER_API_KEY")
        if not self.api_key:
            raise ValueError("TICKETMASTER_API_KEY is required in .env file")
        self.base_url = "https://app.ticketmaster.com/discovery/v2/events.json"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch_events(self, page=0, size=100):
        params = {
            'apikey': self.api_key,
            'city': 'Las Vegas',
            'stateCode': 'NV',
            'size': size,
            'page': page,
            'sort': 'date,asc'
        }
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching Ticketmaster data: {e}")
            return None

    def process_event(self, event_data):
        try:
            # Extract and normalize data
            category = event_data.get('classifications', [{}])[0].get('segment', {}).get('name', "Event")
            normalized_category = CATEGORY_MAPPING.get(category, category)

            return {
                'external_id': event_data['id'],
                'name': event_data.get('name'),
                'description': event_data.get('description', ''),
                'category': normalized_category,
                'subcategory': event_data.get('classifications', [{}])[0].get('genre', {}).get('name'),
                'price_range_min': event_data.get('priceRanges', [{}])[0].get('min'),
                'price_range_max': event_data.get('priceRanges', [{}])[0].get('max'),
                'venue': event_data.get('_embedded', {}).get('venues', [{}])[0].get('name'),
                'start_date': datetime.fromisoformat(event_data.get('dates', {}).get('start', {}).get('dateTime', '').replace('Z', '+00:00')),
                'image_url': max(event_data.get('images', []), key=lambda x: int(x.get('width', 0)) * int(x.get('height', 0))).get('url'),
                'source': 'ticketmaster'
            }
        except Exception as e:
            logging.error(f"Error processing event {event_data.get('id')}: {e}")
            return None

    def ingest_data(self):
        with app.app_context():
            try:
                page = 0
                total_processed = 0
                while True:
                    print(f"Fetching page {page}...")
                    response_data = self.fetch_events(page=page)
                    if not response_data or '_embedded' not in response_data:
                        break

                    events = response_data['_embedded'].get('events', [])
                    if not events:
                        break

                    for event_data in events:
                        processed_event = self.process_event(event_data)
                        if not processed_event:
                            continue

                        event = Event.query.filter_by(external_id=processed_event['external_id']).first()
                        if event:
                            for key, value in processed_event.items():
                                setattr(event, key, value)
                        else:
                            event = Event(**processed_event)
                            db.session.add(event)

                        total_processed += 1

                    db.session.commit()
                    print(f"Processed {len(events)} events on page {page}")
                    page += 1

                print(f"✅ Successfully processed {total_processed} events")
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error during ingestion: {e}")
                raise e

def main():
    logging.basicConfig(level=logging.INFO)
    service = EventIngestionService()
    service.ingest_data()

if __name__ == "__main__":
    main()