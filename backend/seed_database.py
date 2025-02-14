import sys
import os
from datetime import datetime, timedelta
import bcrypt
import pyotp
from app import app, db, User, Event, UserPreference, UserInteraction

def seed_database():
    """Seed the database with sample data"""
    with app.app_context():
        try:
            print("Clearing existing data...")
            UserInteraction.query.delete()
            UserPreference.query.delete()
            Event.query.delete()
            User.query.delete()
            db.session.commit()

            print("Creating test user...")
            # Create test user with 2FA
            test_password = "test123"
            password_hash = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            otp_secret = pyotp.random_base32()
            
            test_user = User(
                username="testuser",
                password_hash=password_hash,
                otp_secret=otp_secret
            )
            db.session.add(test_user)
            db.session.commit()

            print(f"Test user created! OTP Secret: {otp_secret}")
            totp = pyotp.TOTP(otp_secret)
            print(f"Current OTP code: {totp.now()}")

            print("Adding sample events...")
            # Add sample events
            events = [
                {
                    "external_id": "TM123",
                    "name": "Cirque du Soleil - O",
                    "description": "Aquatic theatrical masterpiece at the Bellagio",
                    "category": "Shows",
                    "subcategory": "Circus",
                    "price_range_min": 99.00,
                    "price_range_max": 299.00,
                    "venue": "Bellagio",
                    "start_date": datetime.now() + timedelta(days=1),
                    "end_date": datetime.now() + timedelta(days=1, hours=2),
                    "image_url": "https://example.com/o-show.jpg",
                    "source": "ticketmaster",
                    "rating": 4.8
                },
                {
                    "external_id": "TM124",
                    "name": "Penn & Teller",
                    "description": "Magic show at Rio All-Suite Hotel & Casino",
                    "category": "Shows",
                    "subcategory": "Magic",
                    "price_range_min": 75.00,
                    "price_range_max": 150.00,
                    "venue": "Rio All-Suite Hotel & Casino",
                    "start_date": datetime.now() + timedelta(days=2),
                    "end_date": datetime.now() + timedelta(days=2, hours=2),
                    "image_url": "https://example.com/penn-teller.jpg",
                    "source": "ticketmaster",
                    "rating": 4.7
                },
                {
                    "external_id": "TM125",
                    "name": "Lady Gaga Residency",
                    "description": "Lady Gaga's Las Vegas Residency Show",
                    "category": "Music",
                    "subcategory": "Pop",
                    "price_range_min": 129.00,
                    "price_range_max": 499.00,
                    "venue": "Park MGM",
                    "start_date": datetime.now() + timedelta(days=3),
                    "end_date": datetime.now() + timedelta(days=3, hours=3),
                    "image_url": "https://example.com/lady-gaga.jpg",
                    "source": "ticketmaster",
                    "rating": 4.9
                }
            ]

            for event_data in events:
                event = Event(**event_data)
                db.session.add(event)
            
            db.session.commit()

            print("Adding user preferences...")
            # Add user preferences
            preferences = [
                {"interest": "Shows", "weight": 5},
                {"interest": "Music", "weight": 4},
                {"interest": "Comedy", "weight": 3}
            ]

            for pref in preferences:
                preference = UserPreference(
                    user_id=test_user.id,
                    interest=pref["interest"],
                    weight=pref["weight"]
                )
                db.session.add(preference)

            db.session.commit()

            print("Adding user interactions...")
            # Add some interactions
            events = Event.query.all()
            interactions = [
                {"event": events[0], "type": "like"},
                {"event": events[1], "type": "view"},
                {"event": events[2], "type": "like"}
            ]

            for interaction in interactions:
                user_interaction = UserInteraction(
                    user_id=test_user.id,
                    event_id=interaction["event"].id,
                    interaction_type=interaction["type"]
                )
                db.session.add(user_interaction)

            db.session.commit()

            print("Database seeded successfully!")
            print("\nTest User Credentials:")
            print("Username: testuser")
            print("Password: test123")
            print(f"OTP Secret: {otp_secret}")
            print(f"Current OTP Code: {totp.now()}")

        except Exception as e:
            print(f"Error seeding database: {str(e)}")
            db.session.rollback()
            raise e

if __name__ == "__main__":
    seed_database()