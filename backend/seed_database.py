import sys
import os
from datetime import datetime, timedelta, time
import bcrypt
import pyotp
from app import (
    app, db, User, Event, UserPreference, UserInteraction, Casino, 
    OutdoorActivity, Affiliate, Review, Tip, LocalGuide, PhotoGallery,
    VirtualTour, Deal, SavedItem, Itinerary, ItineraryItem, WeatherForecast
)

def seed_database():
    """Seed the database with sample data"""
    with app.app_context():
        try:
            print("Clearing existing data...")
            UserInteraction.query.delete()
            UserPreference.query.delete()
            Review.query.delete()
            Tip.query.delete()
            LocalGuide.query.delete()
            PhotoGallery.query.delete()
            VirtualTour.query.delete()
            Deal.query.delete()
            SavedItem.query.delete()
            ItineraryItem.query.delete()
            Itinerary.query.delete()
            WeatherForecast.query.delete()
            Event.query.delete()
            Casino.query.delete()
            OutdoorActivity.query.delete()
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

            print("Adding sample casinos...")
            casinos = [
                {
                    "name": "Bellagio",
                    "description": "Luxury resort, casino and hotel on the Las Vegas Strip",
                    "address": "3600 S Las Vegas Blvd, Las Vegas, NV 89109",
                    "latitude": 36.1126,
                    "longitude": -115.1767,
                    "rating": 4.7,
                    "review_count": 45000,
                    "amenities": ["Fine Dining", "Luxury Shops", "Spa", "Pool", "Fountain Show"],
                    "restaurants": ["Le Cirque", "Picasso", "Prime Steakhouse"],
                    "shows": ["O by Cirque du Soleil"],
                    "gaming_options": ["Slots", "Table Games", "High Limit Room", "Poker Room"],
                    "parking_info": "Free self-parking and valet available for guests",
                    "website": "https://bellagio.mgmresorts.com",
                    "affiliate_link": "https://example.com/affiliate/bellagio"
                },
                {
                    "name": "Red Rock Casino",
                    "description": "Luxury resort near Red Rock Canyon",
                    "address": "11011 W Charleston Blvd, Las Vegas, NV 89135",
                    "latitude": 36.1578,
                    "longitude": -115.3347,
                    "rating": 4.6,
                    "review_count": 25000,
                    "amenities": ["Movie Theater", "Bowling Alley", "Spa", "Pool"],
                    "restaurants": ["T-Bones Chophouse", "Hearthstone", "Blue Ribbon Sushi"],
                    "shows": ["Live Music at Rocks Lounge"],
                    "gaming_options": ["Slots", "Table Games", "Sports Book", "Bingo"],
                    "parking_info": "Free parking available",
                    "website": "https://redrock.sclv.com",
                    "affiliate_link": "https://example.com/affiliate/redrock"
                }
            ]

            for casino_data in casinos:
                casino = Casino(**casino_data)
                db.session.add(casino)

            print("Adding sample outdoor activities...")
            outdoor_activities = [
                {
                    "name": "Red Rock Canyon Scenic Drive",
                    "description": "13-mile scenic drive through Red Rock Canyon National Conservation Area",
                    "category": "scenic-drives",
                    "difficulty_level": "easy",
                    "distance": 13.0,
                    "elevation_gain": 1000,
                    "latitude": 36.1357,
                    "longitude": -115.4277,
                    "best_seasons": ["spring", "fall", "winter"],
                    "parking_available": True,
                    "amenities": ["Visitor Center", "Picnic Areas", "Restrooms"],
                    "tour_operators": ["Pink Jeep Tours", "Red Rock Canyon Tours"],
                    "affiliate_links": {
                        "tours": "https://example.com/affiliate/redrock-tours",
                        "parking_pass": "https://example.com/affiliate/redrock-pass"
                    }
                },
                {
                    "name": "Lake Mead Kayaking",
                    "description": "Kayaking adventure on Lake Mead with stunning views",
                    "category": "water-sports",
                    "difficulty_level": "moderate",
                    "distance": 5.0,
                    "elevation_gain": 0,
                    "latitude": 36.1515,
                    "longitude": -114.8470,
                    "best_seasons": ["spring", "summer", "fall"],
                    "parking_available": True,
                    "amenities": ["Boat Launch", "Restrooms", "Picnic Areas"],
                    "tour_operators": ["Desert Adventures", "Evolution Expeditions"],
                    "affiliate_links": {
                        "kayak_rental": "https://example.com/affiliate/kayak-rental",
                        "guided_tour": "https://example.com/affiliate/kayak-tour"
                    }
                }
            ]

            for activity_data in outdoor_activities:
                activity = OutdoorActivity(**activity_data)
                db.session.add(activity)

            print("Adding sample events...")
            events = [
                {
                    "external_id": "TM123",
                    "name": "Cirque du Soleil - O",
                    "description": "Aquatic theatrical masterpiece at the Bellagio",
                    "category": "cirque",
                    "subcategory": "Circus",
                    "price_range_min": 99.00,
                    "price_range_max": 299.00,
                    "venue": "Bellagio",
                    "start_date": datetime.now() + timedelta(days=1),
                    "end_date": datetime.now() + timedelta(days=1, hours=2),
                    "image_url": "https://example.com/o-show.jpg",
                    "source": "ticketmaster",
                    "rating": 4.8,
                    "review_count": 2500,
                    "latitude": 36.1126,
                    "longitude": -115.1767,
                    "address": "3600 S Las Vegas Blvd, Las Vegas, NV 89109",
                    "tags": ["entertainment", "circus", "water", "acrobatics"],
                    "url": "https://www.bellagio.com/en/entertainment/o-cirque-du-soleil.html",
                    "casino": "Bellagio",
                    "age_restriction": 5,
                    "dress_code": "Smart Casual",
                    "parking_info": "Valet and self-parking available",
                    "reservation_required": True,
                    "indoor_outdoor": "indoor",
                    "typical_duration": 90,
                    "best_times": ["evening"],
                    "amenities": ["Wheelchair Accessible", "Concessions", "Gift Shop"],
                    "weather_dependent": False,
                    "affiliate_links": {
                        "tickets": "https://example.com/affiliate/o-show-tickets"
                    }
                },
                {
                    "external_id": "RR001",
                    "name": "Red Rock Canyon Hiking Tour",
                    "description": "Guided hiking tour through Red Rock Canyon's most scenic trails",
                    "category": "hiking",
                    "subcategory": "Guided Tour",
                    "price_range_min": 75.00,
                    "price_range_max": 150.00,
                    "venue": "Red Rock Canyon",
                    "start_date": datetime.now() + timedelta(days=2),
                    "end_date": datetime.now() + timedelta(days=2, hours=4),
                    "image_url": "https://example.com/redrock-hiking.jpg",
                    "source": "direct",
                    "rating": 4.9,
                    "review_count": 850,
                    "latitude": 36.1357,
                    "longitude": -115.4277,
                    "address": "Red Rock Canyon National Conservation Area",
                    "tags": ["outdoor", "hiking", "nature", "adventure"],
                    "url": "https://example.com/redrock-hiking",
                    "age_restriction": None,
                    "dress_code": "Athletic Wear",
                    "parking_info": "Parking pass required",
                    "reservation_required": True,
                    "indoor_outdoor": "outdoor",
                    "typical_duration": 240,
                    "best_times": ["morning", "afternoon"],
                    "amenities": ["Guide", "Water", "Snacks", "Transportation"],
                    "difficulty_level": "moderate",
                    "seasonal_info": "Best in spring and fall. Limited tours in summer due to heat.",
                    "weather_dependent": True,
                    "affiliate_links": {
                        "tour_booking": "https://example.com/affiliate/redrock-hiking-tour",
                        "gear_rental": "https://example.com/affiliate/hiking-gear"
                    }
                },
                {
                    "external_id": "GP001",
                    "name": "High Roller Happy Half Hour",
                    "description": "Open bar during 30-minute ride on world's tallest observation wheel",
                    "category": "attractions",
                    "subcategory": "Observation Wheel",
                    "price_range_min": 60.00,
                    "price_range_max": 85.00,
                    "venue": "The LINQ",
                    "start_date": datetime.now(),
                    "end_date": datetime.now() + timedelta(days=365),
                    "image_url": "https://example.com/high-roller.jpg",
                    "source": "direct",
                    "rating": 4.6,
                    "review_count": 1500,
                    "latitude": 36.1173,
                    "longitude": -115.1711,
                    "address": "3545 S Las Vegas Blvd, Las Vegas, NV 89109",
                    "tags": ["drinks", "views", "nightlife", "attractions"],
                    "url": "https://example.com/high-roller",
                    "age_restriction": 21,
                    "dress_code": "Casual",
                    "parking_info": "LINQ Parking Garage",
                    "reservation_required": False,
                    "indoor_outdoor": "both",
                    "typical_duration": 30,
                    "best_times": ["sunset", "night"],
                    "amenities": ["Bar", "Air Conditioning", "Photo Op"],
                    "weather_dependent": False,
                    "affiliate_links": {
                        "tickets": "https://example.com/affiliate/high-roller"
                    }
                }
            ]

            for event_data in events:
                event = Event(**event_data)
                db.session.add(event)

            print("Adding sample reviews...")
            reviews = [
                {
                    "user_id": test_user.id,
                    "event_id": 1,  # Will be set after events are created
                    "rating": 5,
                    "title": "Spectacular Show!",
                    "content": "O by Cirque du Soleil was absolutely breathtaking. The water acrobatics were unlike anything I've ever seen.",
                    "visit_date": datetime.now() - timedelta(days=5),
                    "photos": ["https://example.com/review1-photo1.jpg", "https://example.com/review1-photo2.jpg"],
                    "helpful_votes": 25,
                    "verified_purchase": True
                },
                {
                    "user_id": test_user.id,
                    "outdoor_activity_id": 1,  # Will be set after outdoor activities are created
                    "rating": 4,
                    "title": "Beautiful Hiking Experience",
                    "content": "Red Rock Canyon offers stunning views and well-maintained trails. Go early to avoid the heat!",
                    "visit_date": datetime.now() - timedelta(days=3),
                    "photos": ["https://example.com/review2-photo1.jpg"],
                    "helpful_votes": 12,
                    "verified_purchase": True
                }
            ]

            print("Adding sample tips...")
            tips = [
                {
                    "user_id": test_user.id,
                    "category": "saving_money",
                    "title": "Best Time to Book Shows",
                    "content": "Book Cirque du Soleil shows 2-3 months in advance for the best deals. Many hotels offer package deals that include show tickets.",
                    "tags": ["shows", "cirque-du-soleil", "deals", "booking"],
                    "helpful_votes": 45,
                    "verified": True
                },
                {
                    "user_id": test_user.id,
                    "category": "best_time",
                    "title": "Hiking in Red Rock Canyon",
                    "content": "The best time for hiking is early morning (6-9am) during summer months. Winter afternoons are also pleasant.",
                    "tags": ["outdoor", "hiking", "weather", "red-rock"],
                    "helpful_votes": 32,
                    "verified": True
                }
            ]

            print("Adding sample local guides...")
            guides = [
                {
                    "title": "Ultimate Guide to Las Vegas Shows",
                    "content": "Comprehensive guide to all major shows on the Strip...",
                    "category": "entertainment",
                    "author_id": test_user.id,
                    "featured_image": "https://example.com/vegas-shows-guide.jpg",
                    "tags": ["shows", "entertainment", "cirque-du-soleil", "magic-shows"],
                    "views": 1200,
                    "likes": 89
                },
                {
                    "title": "Outdoor Adventures Near Las Vegas",
                    "content": "Discover the natural wonders just minutes from the Strip...",
                    "category": "outdoor",
                    "author_id": test_user.id,
                    "featured_image": "https://example.com/vegas-outdoor-guide.jpg",
                    "tags": ["hiking", "red-rock", "lake-mead", "outdoor-activities"],
                    "views": 850,
                    "likes": 67
                }
            ]

            print("Adding sample virtual tours...")
            tours = [
                {
                    "title": "Bellagio Conservatory Virtual Tour",
                    "description": "Explore the stunning seasonal displays at the Bellagio Conservatory",
                    "venue_name": "Bellagio",
                    "tour_type": "360",
                    "media_url": "https://example.com/virtual-tours/bellagio-conservatory",
                    "thumbnail_url": "https://example.com/virtual-tours/bellagio-thumb.jpg",
                    "duration": 600,
                    "views": 3500
                },
                {
                    "title": "Red Rock Canyon Scenic Drive",
                    "description": "Take a virtual drive through the stunning Red Rock Canyon",
                    "venue_name": "Red Rock Canyon",
                    "tour_type": "video",
                    "media_url": "https://example.com/virtual-tours/red-rock-drive",
                    "thumbnail_url": "https://example.com/virtual-tours/red-rock-thumb.jpg",
                    "duration": 900,
                    "views": 2800
                }
            ]

            print("Adding sample deals...")
            deals = [
                {
                    "title": "2-for-1 Cirque du Soleil Tickets",
                    "description": "Buy one ticket, get one free for select Cirque du Soleil shows",
                    "deal_type": "special_offer",
                    "venue": "Multiple Venues",
                    "start_date": datetime.now(),
                    "end_date": datetime.now() + timedelta(days=30),
                    "terms": "Valid for select shows. Subject to availability.",
                    "promo_code": "CIRQUE241",
                    "discount_type": "percentage",
                    "discount_amount": 50.00,
                    "min_purchase": 129.00,
                    "max_discount": 299.00,
                    "redemption_count": 145,
                    "active": True,
                    "affiliate_link": "https://example.com/affiliate/cirque-deal"
                },
                {
                    "title": "Red Rock Canyon Tour Package",
                    "description": "Guided tour + lunch + transportation",
                    "deal_type": "package",
                    "venue": "Red Rock Canyon",
                    "start_date": datetime.now(),
                    "end_date": datetime.now() + timedelta(days=90),
                    "terms": "24-hour cancellation policy applies",
                    "promo_code": "REDROCK20",
                    "discount_type": "percentage",
                    "discount_amount": 20.00,
                    "min_purchase": 75.00,
                    "max_discount": 150.00,
                    "redemption_count": 89,
                    "active": True,
                    "affiliate_link": "https://example.com/affiliate/redrock-deal"
                }
            ]

            print("Adding sample itineraries...")
            itinerary = Itinerary(
                user_id=test_user.id,
                title="Perfect Vegas Weekend",
                description="3-day itinerary combining shows, outdoor activities, and fine dining",
                start_date=datetime.now() + timedelta(days=30),
                end_date=datetime.now() + timedelta(days=33),
                is_public=True,
                likes=25
            )
            db.session.add(itinerary)
            db.session.flush()  # Get the itinerary ID

            # Add itinerary items after creating the itinerary
            itinerary_items = [
                {
                    "itinerary_id": itinerary.id,
                    "item_type": "event",
                    "item_id": 1,  # O Show
                    "day_number": 1,
                    "start_time": time(19, 30),  # 7:30 PM
                    "duration": 90,
                    "notes": "Arrive 30 minutes early. Smart casual dress code."
                },
                {
                    "itinerary_id": itinerary.id,
                    "item_type": "outdoor_activity",
                    "item_id": 1,  # Red Rock Canyon
                    "day_number": 2,
                    "start_time": time(8, 0),  # 8:00 AM
                    "duration": 240,
                    "notes": "Bring water and sunscreen. Wear hiking shoes."
                }
            ]

            for item_data in itinerary_items:
                item = ItineraryItem(**item_data)
                db.session.add(item)

            print("Adding sample weather forecasts...")
            for i in range(7):  # Next 7 days
                forecast = WeatherForecast(
                    date=datetime.now().date() + timedelta(days=i),
                    temperature_high=95 + i,
                    temperature_low=65 + i,
                    conditions="Sunny" if i % 2 == 0 else "Partly Cloudy",
                    precipitation_chance=0.1 if i % 2 == 0 else 0.3,
                    wind_speed=8.0 + i
                )
                db.session.add(forecast)

            print("Adding sample affiliates...")
            affiliates = [
                {
                    "name": "Vegas.com",
                    "website": "https://www.vegas.com",
                    "api_key": "sample_key_1",
                    "commission_rate": 0.08,
                    "categories": ["shows", "hotels", "attractions"],
                    "active": True
                },
                {
                    "name": "Viator",
                    "website": "https://www.viator.com",
                    "api_key": "sample_key_2",
                    "commission_rate": 0.10,
                    "categories": ["tours", "activities", "day-trips"],
                    "active": True
                }
            ]

            for affiliate_data in affiliates:
                affiliate = Affiliate(**affiliate_data)
                db.session.add(affiliate)
            
            db.session.commit()

            print("Adding user preferences...")
            # Add user preferences
            preferences = [
                {"interest": "shows", "weight": 5},
                {"interest": "outdoor", "weight": 4},
                {"interest": "nightlife", "weight": 3}
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

            # Update review references after creating main entities
            events = Event.query.all()
            outdoor_activities_db = OutdoorActivity.query.all()
            
            if events and outdoor_activities_db:
                reviews[0]["event_id"] = events[0].id
                reviews[1]["outdoor_activity_id"] = outdoor_activities_db[0].id

                for review_data in reviews:
                    review = Review(**review_data)
                    db.session.add(review)

                db.session.commit()

            print("Content management data seeded successfully!")
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