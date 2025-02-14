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
db_user = os.environ.get('DB_USER', 'myuser')
db_password = os.environ.get('DB_PASSWORD', 'mypassword')
db_name = os.environ.get('DB_NAME', 'las_vegas_db')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', '5432')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    interactions = db.relationship('UserInteraction', backref='event', lazy=True)

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

# Recommendation Engine
class RecommendationEngine:
    def get_personalized_recommendations(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return []

        # Get user preferences
        preferences = {pref.interest: pref.weight for pref in user.preferences}

        # Get user interactions
        interactions = UserInteraction.query.filter_by(user_id=user_id).all()
        liked_events = [interaction.event_id for interaction in interactions if interaction.interaction_type == 'like']

        # Query events matching preferences
        query = Event.query.filter(Event.start_date >= datetime.utcnow())
        if preferences:
            query = query.filter(Event.category.in_(preferences.keys()))
        events = query.order_by(Event.start_date).limit(100).all()

        # Score events based on preferences and interactions
        scored_events = []
        for event in events:
            score = preferences.get(event.category, 1)
            if event.id in liked_events:
                score *= 2  # Boost score for liked events
            scored_events.append((event, score))

        # Sort by score and return top recommendations
        scored_events.sort(key=lambda x: x[1], reverse=True)
        return [event for event, score in scored_events[:20]]

# Caching
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
        # Get filter parameters
        category = request.args.get('category')
        price_range = request.args.get('priceRange')
        timeframe = request.args.get('timeframe')
        
        # Base query
        query = Event.query.filter(Event.start_date >= datetime.utcnow())
        
        # Apply filters
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
        
        # Get results
        events = query.order_by(Event.start_date).limit(100).all()
        
        # Format response
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
                "source": event.source
            })
        
        return jsonify(response)
    except Exception as e:
        print(f"Error fetching events: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/events/<int:event_id>", methods=["GET"])
def get_event_details(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        
        # Record view interaction if user is logged in
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

# Recommendation Routes
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

# Home Route
@app.route('/')
def index():
    return "Welcome to Las Vegas AI!"

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)