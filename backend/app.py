import os
from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt
import pyotp
from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import UUID
import uuid
from functools import lru_cache
from tenacity import retry, stop_after_attempt, wait_exponential
import requests
import logging

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_secret_key')  # Change in production
CORS(app, supports_credentials=True)

# Database configuration
db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/vegas_ai')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database Models
class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime)
    venue = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    otp_secret = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    preferences = db.relationship('UserPreference', backref='user', lazy=True)
    interactions = db.relationship('UserInteraction', backref='user', lazy=True)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    subcategory = db.Column(db.String(100))
    price_range_min = db.Column(db.Numeric(10, 2))
    price_range_max = db.Column(db.Numeric(10, 2))
    venue = db.Column(db.String(255))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    image_url = db.Column(db.Text)
    source = db.Column(db.String(50))
    rating = db.Column(db.Numeric(3, 2))
    review_count = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.Text)
    tags = db.Column(db.ARRAY(db.String))
    url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    interactions = db.relationship('UserInteraction', backref='event', lazy=True)
    raw_data = db.Column(db.dialects.postgresql.JSONB)
    
    # New Vegas-specific fields
    casino = db.Column(db.String(255))
    age_restriction = db.Column(db.Integer)
    dress_code = db.Column(db.String(100))
    parking_info = db.Column(db.Text)
    reservation_required = db.Column(db.Boolean, default=False)
    indoor_outdoor = db.Column(db.String(20))
    typical_duration = db.Column(db.Integer)  # in minutes
    best_times = db.Column(db.ARRAY(db.String))
    amenities = db.Column(db.ARRAY(db.String))
    difficulty_level = db.Column(db.String(20))
    seasonal_info = db.Column(db.Text)
    weather_dependent = db.Column(db.Boolean, default=False)
    popularity_score = db.Column(db.Float, default=0.0)
    affiliate_links = db.Column(db.dialects.postgresql.JSONB)
    
    def __repr__(self):
        return f"<Event {self.name}>"

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    interest = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserInteraction(db.Model):
    __tablename__ = 'user_interactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    interaction_type = db.Column(db.String(50), nullable=False)  # 'view', 'like', 'dislike'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.String(50))
    source = db.Column(db.String(255))
    message = db.Column(db.Text)

# New models for monetization and enhanced features
class Casino(db.Model):
    __tablename__ = 'casinos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    rating = db.Column(db.Numeric(3, 2))
    review_count = db.Column(db.Integer)
    amenities = db.Column(db.ARRAY(db.String))
    restaurants = db.Column(db.ARRAY(db.String))
    shows = db.Column(db.ARRAY(db.String))
    gaming_options = db.Column(db.ARRAY(db.String))
    parking_info = db.Column(db.Text)
    website = db.Column(db.Text)
    affiliate_link = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class OutdoorActivity(db.Model):
    __tablename__ = 'outdoor_activities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    difficulty_level = db.Column(db.String(20))
    distance = db.Column(db.Float)  # in miles
    elevation_gain = db.Column(db.Float)  # in feet
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    best_seasons = db.Column(db.ARRAY(db.String))
    parking_available = db.Column(db.Boolean)
    amenities = db.Column(db.ARRAY(db.String))
    tour_operators = db.Column(db.ARRAY(db.String))
    affiliate_links = db.Column(db.dialects.postgresql.JSONB)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Affiliate(db.Model):
    __tablename__ = 'affiliates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    website = db.Column(db.Text)
    api_key = db.Column(db.String(255))
    commission_rate = db.Column(db.Float)
    categories = db.Column(db.ARRAY(db.String))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AffiliateClick(db.Model):
    __tablename__ = 'affiliate_clicks'
    id = db.Column(db.Integer, primary_key=True)
    affiliate_id = db.Column(db.Integer, db.ForeignKey('affiliates.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    click_time = db.Column(db.DateTime, default=datetime.utcnow)
    converted = db.Column(db.Boolean, default=False)
    commission_amount = db.Column(db.Numeric(10, 2))

class Advertisement(db.Model):
    __tablename__ = 'advertisements'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.Text)
    target_url = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    categories = db.Column(db.ARRAY(db.String))
    price_paid = db.Column(db.Numeric(10, 2))
    impressions = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AdClick(db.Model):
    __tablename__ = 'ad_clicks'
    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('advertisements.id'))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    click_time = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)

class UserSubscription(db.Model):
    __tablename__ = 'user_subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    plan_type = db.Column(db.String(50))  # 'free', 'premium', 'business'
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    auto_renew = db.Column(db.Boolean, default=True)
    payment_method = db.Column(db.String(50))
    amount_paid = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(50))  # 'active', 'cancelled', 'expired'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Content Management Models
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)
    casino_id = db.Column(db.Integer, db.ForeignKey('casinos.id'), nullable=True)
    outdoor_activity_id = db.Column(db.Integer, db.ForeignKey('outdoor_activities.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    title = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    visit_date = db.Column(db.DateTime)
    photos = db.Column(db.ARRAY(db.String))  # Array of photo URLs
    helpful_votes = db.Column(db.Integer, default=0)
    verified_purchase = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class Tip(db.Model):
    __tablename__ = 'tips'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # e.g., 'saving_money', 'best_time', 'insider'
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.ARRAY(db.String))
    helpful_votes = db.Column(db.Integer, default=0)
    verified = db.Column(db.Boolean, default=False)  # Verified by moderators
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LocalGuide(db.Model):
    __tablename__ = 'local_guides'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    featured_image = db.Column(db.String(255))
    tags = db.Column(db.ARRAY(db.String))
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class PhotoGallery(db.Model):
    __tablename__ = 'photo_galleries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)
    casino_id = db.Column(db.Integer, db.ForeignKey('casinos.id'), nullable=True)
    outdoor_activity_id = db.Column(db.Integer, db.ForeignKey('outdoor_activities.id'), nullable=True)
    photo_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.Text)
    taken_at = db.Column(db.DateTime)
    likes = db.Column(db.Integer, default=0)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VirtualTour(db.Model):
    __tablename__ = 'virtual_tours'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    venue_name = db.Column(db.String(255), nullable=False)
    tour_type = db.Column(db.String(50))  # '360', 'video', 'interactive'
    media_url = db.Column(db.String(255), nullable=False)
    thumbnail_url = db.Column(db.String(255))
    duration = db.Column(db.Integer)  # in seconds
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Deal(db.Model):
    __tablename__ = 'deals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    deal_type = db.Column(db.String(50))  # 'discount', 'package', 'special_offer'
    venue = db.Column(db.String(255))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    terms = db.Column(db.Text)
    promo_code = db.Column(db.String(50))
    discount_amount = db.Column(db.Numeric(10, 2))
    discount_type = db.Column(db.String(20))  # 'percentage', 'fixed'
    min_purchase = db.Column(db.Numeric(10, 2))
    max_discount = db.Column(db.Numeric(10, 2))
    redemption_count = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    affiliate_link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SavedItem(db.Model):
    __tablename__ = 'saved_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)  # 'event', 'casino', 'outdoor_activity', 'deal'
    item_id = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Itinerary(db.Model):
    __tablename__ = 'itineraries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    is_public = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class ItineraryItem(db.Model):
    __tablename__ = 'itinerary_items'
    id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    day_number = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time)
    duration = db.Column(db.Integer)  # in minutes
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WeatherForecast(db.Model):
    __tablename__ = 'weather_forecasts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    temperature_high = db.Column(db.Float)
    temperature_low = db.Column(db.Float)
    conditions = db.Column(db.String(100))
    precipitation_chance = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Add relationships to existing models
Event.reviews = db.relationship('Review', backref='event', lazy=True,
                              foreign_keys=[Review.event_id])
Casino.reviews = db.relationship('Review', backref='casino', lazy=True,
                               foreign_keys=[Review.casino_id])
OutdoorActivity.reviews = db.relationship('Review', backref='outdoor_activity', lazy=True,
                                        foreign_keys=[Review.outdoor_activity_id])

# Recommendation Engine
class RecommendationEngine:
    def get_personalized_recommendations(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return []

        preferences = {pref.interest: pref.weight for pref in user.preferences}
        interactions = UserInteraction.query.filter_by(user_id=user_id).all()
        liked_events = [interaction.event_id for interaction in interactions if interaction.interaction_type == 'like']

        query = Event.query.filter(Event.start_date >= datetime.utcnow())
        if preferences:
            query = query.filter(Event.category.in_(preferences.keys()))
        events = query.order_by(Event.start_date).limit(100).all()

        scored_events = []
        for event in events:
            score = preferences.get(event.category, 1)
            if event.id in liked_events:
                score *= 2
            scored_events.append((event, score))

        scored_events.sort(key=lambda x: x[1], reverse=True)
        return [event for event, score in scored_events[:20]]

@lru_cache(maxsize=100)
def get_cached_recommendations(user_id):
    engine = RecommendationEngine()
    return engine.get_personalized_recommendations(user_id)

# Authentication Routes
@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    otp_code = data.get("otp")
    
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        totp = pyotp.TOTP(user.otp_secret)
        if totp.verify(otp_code):
            session["authenticated"] = True
            session["user_id"] = str(user.id)
            return jsonify({"success": True, "message": "Login successful!"})
    
    return jsonify({"success": False, "message": "Invalid credentials or OTP."}), 401

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."})

# Event Routes
@app.route("/api/events", methods=["GET"])
def get_events():
    try:
        category = request.args.get('category')
        price_range = request.args.get('priceRange')
        timeframe = request.args.get('timeframe')
        source = request.args.get('source')
        min_rating = request.args.get('min_rating', type=float)
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        radius = request.args.get('radius', type=float)  # in kilometers

        query = Event.query.filter(Event.start_date >= datetime.utcnow())

        if category:
            query = query.filter(Event.category == category)
        if price_range == 'free':
            query = query.filter(Event.price_range_min == 0)
        elif price_range == 'paid':
            query = query.filter(Event.price_range_min > 0)
        if timeframe == 'today':
            end_date = datetime.utcnow() + timedelta(days=1)
            query = query.filter(Event.start_date <= end_date)
        elif timeframe == 'week':
            end_date = datetime.utcnow() + timedelta(days=7)
            query = query.filter(Event.start_date <= end_date)
        elif timeframe == 'month':
            end_date = datetime.utcnow() + timedelta(days=30)
            query = query.filter(Event.start_date <= end_date)
        if source:
            query = query.filter(Event.source.ilike(source))
        if min_rating:
            query = query.filter(Event.rating >= min_rating)

        # Location-based filtering using Haversine formula
        if latitude is not None and longitude is not None and radius is not None:
            # Convert radius from kilometers to degrees (approximate)
            radius_degrees = radius / 111.0  # 1 degree ≈ 111 km
            query = query.filter(
                db.and_(
                    Event.latitude.isnot(None),
                    Event.longitude.isnot(None),
                    db.func.acos(
                        db.func.sin(db.func.radians(latitude)) *
                        db.func.sin(db.func.radians(Event.latitude)) +
                        db.func.cos(db.func.radians(latitude)) *
                        db.func.cos(db.func.radians(Event.latitude)) *
                        db.func.cos(db.func.radians(longitude) - db.func.radians(Event.longitude))
                    ) * 6371 <= radius  # 6371 is Earth's radius in kilometers
                )
            )

        events = query.order_by(Event.start_date).limit(100).all()
        response = []
        for event in events:
            response.append({
                "id": event.id,
                "name": event.name,
                "description": event.description,
                "category": event.category,
                "subcategory": event.subcategory,
                "price_range_min": float(event.price_range_min) if event.price_range_min else None,
                "price_range_max": float(event.price_range_max) if event.price_range_max else None,
                "venue": event.venue,
                "start_date": event.start_date.isoformat() if event.start_date else None,
                "end_date": event.end_date.isoformat() if event.end_date else None,
                "image_url": event.image_url,
                "source": event.source,
                "rating": float(event.rating) if event.rating else None,
                "review_count": event.review_count,
                "latitude": event.latitude,
                "longitude": event.longitude,
                "address": event.address,
                "tags": event.tags,
                "url": event.url
            })
        return jsonify(response)
    except Exception as e:
        print(f"Error fetching events: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/events/<int:event_id>", methods=["GET"])
def get_event_details(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        if "user_id" in session:
            interaction = UserInteraction(
                user_id=session["user_id"],
                event_id=event.id,
                interaction_type='view'
            )
            db.session.add(interaction)
            db.session.commit()
        return jsonify({
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "category": event.category,
            "subcategory": event.subcategory,
            "price_range_min": float(event.price_range_min) if event.price_range_min else None,
            "price_range_max": float(event.price_range_max) if event.price_range_max else None,
            "venue": event.venue,
            "start_date": event.start_date.isoformat() if event.start_date else None,
            "end_date": event.end_date.isoformat() if event.end_date else None,
            "image_url": event.image_url,
            "source": event.source
        })
    except Exception as e:
        print(f"Error fetching event details: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/events/<int:event_id>/interact", methods=["POST"])
def record_event_interaction(event_id):
    if "user_id" not in session:
        return jsonify({"error": "User not logged in"}), 401
    try:
        interaction_type = request.json.get('type', 'view')
        if interaction_type not in ['view', 'like', 'dislike']:
            return jsonify({"error": "Invalid interaction type"}), 400
        interaction = UserInteraction(
            user_id=session["user_id"],
            event_id=event_id,
            interaction_type=interaction_type
        )
        db.session.add(interaction)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error recording interaction: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/recommendations", methods=["GET"])
def get_recommendations():
    if "user_id" not in session:
        return jsonify({"error": "User not logged in"}), 401
    recommendations = get_cached_recommendations(session["user_id"])
    return jsonify([{
        "id": event.id,
        "name": event.name,
        "category": event.category,
        "start_date": event.start_date.isoformat() if event.start_date else None,
        "image_url": event.image_url
    } for event in recommendations])

@app.route("/view-recommendations")
def view_recommendations():
    events = Event.query.filter(Event.start_date >= datetime.utcnow()).order_by(Event.start_date).limit(50).all()
    return render_template("recommendations.html", recommendations=events)

@app.route('/')
def index():
    return "Welcome to Las Vegas AI!"

from routes.content import content
app.register_blueprint(content, url_prefix='/api/content')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)