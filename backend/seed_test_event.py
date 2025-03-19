import json
from app import app, db, Event
from datetime import datetime

with app.app_context():
    # Create a test event with a populated raw_data field.
    test_event = Event(
        external_id="TEST002",
        name="Test Event with Raw Data",
        description="This event is used for testing the raw_data field.",
        category="Test",
        subcategory="UnitTest",
        price_range_min=10.00,
        price_range_max=20.00,
        venue="Test Venue",
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow(),
        image_url="https://example.com/test.jpg",
        source="manual",
        rating=5,
        raw_data={"sample_key": "sample_value", "another_key": 123}
    )
    db.session.add(test_event)
    db.session.commit()
    print("Test event created with ID:", test_event.id)