import os
import requests
from datetime import datetime
from app import db
from models import Event

def fetch_eventbrite_events():
    """Fetch events from EventBrite API and store them in the database."""
    api_key = os.environ.get("EVENTBRITE_API_KEY")
    if not api_key:
        raise Exception("EVENTBRITE_API_KEY is not set in environment variables.")

    headers = {"Authorization": f"Bearer {api_key}"}
    # Customize the search parameters as needed
    url = "https://www.eventbriteapi.com/v3/events/search/"
    params = {
        "location.address": "Las Vegas",
        "expand": "venue",
        "sort_by": "date"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch events: {response.status_code} - {response.text}")

    events_data = response.json().get("events", [])
    for event in events_data:
        # Map EventBrite fields to your Event model
        external_id = event.get("id")
        name = event.get("name", {}).get("text")
        description = event.get("description", {}).get("text")
        
        # Parse dates (assuming ISO 8601 format)
        start_date_str = event.get("start", {}).get("local")
        end_date_str = event.get("end", {}).get("local")
        start_date = datetime.fromisoformat(start_date_str) if start_date_str else None
        end_date = datetime.fromisoformat(end_date_str) if end_date_str else None

        # Retrieve venue name if available
        venue = None
        if event.get("venue"):
            venue = event["venue"].get("name")
        
        # Price information may not be available or might require additional API calls
        price_range_min = None
        price_range_max = None
        
        # Get image URL if available
        image_url = event.get("logo", {}).get("url")

        # Set the source field to differentiate this event as coming from EventBrite
        source = "eventbrite"

        # Check for duplicate events using external_id to avoid conflicts
        if Event.query.filter_by(external_id=external_id, source=source).first():
            continue  # Skip if the event already exists

        new_event = Event(
            external_id=external_id,
            name=name,
            description=description,
            venue=venue,
            start_date=start_date,
            end_date=end_date,
            image_url=image_url,
            source=source,
            # Set other fields as necessary (e.g., category, rating)
        )
        db.session.add(new_event)
    
    db.session.commit()
    print(f"Imported {len(events_data)} events from EventBrite.")