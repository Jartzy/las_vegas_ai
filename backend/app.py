# backend/app.py
import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt
import pyotp

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change in production
CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'postgresql://myuser:mypassword@db/las_vegas_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Extended User model remains the same...
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    otp_secret = db.Column(db.String(16), nullable=False)

# Extended Recommendation model to include additional fields:
class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)          # New field: event description
    event_date = db.Column(db.DateTime)         # New field: event start date/time
    venue = db.Column(db.String(255))           # New field: venue name
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

# -------------------------
# Routes / Endpoints
# -------------------------

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
            session["user_id"] = user.id
            return jsonify({"success": True, "message": "Login successful!"})
    
    return jsonify({"success": False, "message": "Invalid credentials or OTP."}), 401

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."})

@app.route("/api/recommendations", methods=["GET"])
def get_recommendations():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in."}), 403

    recs = Recommendation.query.order_by(Recommendation.created_at.desc()).limit(10).all()
    recommendations = [{"id": rec.id, "name": rec.name, "category": rec.category} for rec in recs]
    return jsonify(recommendations)

# A simple route for testing
@app.route('/')
def index():
    return "Welcome to Las Vegas AI!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)