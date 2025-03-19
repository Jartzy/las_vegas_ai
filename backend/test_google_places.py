import os
from app import app, db, Event

def test_google_places_events():
    with app.app_context():
        # Query for events where the source is 'google_places'
        events = Event.query.filter(Event.source.ilike("google_places")).all()
        
        if not events:
            print("No Google Places events found in the database.")
        else:
            print(f"Found {len(events)} Google Places event(s):")
            for event in events:
                print(f"ID: {event.id}, Name: {event.name}, Start Date: {event.start_date}, Source: {event.source}")

if __name__ == "__main__":
    test_google_places_events()