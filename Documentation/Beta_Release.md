Adding Two-Factor Authentication (2FA) for Extra Security

To enhance security, we’ll implement 2FA using Google Authenticator (TOTP - Time-based One-Time Passwords).

1. Install Required Packages

pip install pyotp qrcode[pil]

2. Update users Table to Store 2FA Secret

Modify your PostgreSQL schema to include a column for the 2FA secret key.

ALTER TABLE users ADD COLUMN otp_secret TEXT;

3. Update User Creation (database.py)

Modify user registration to generate a unique 2FA secret.

import pyotp
import psycopg2
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
DATABASE_URL = "postgresql://myuser:mypassword@db/las_vegas_db"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def create_user(username, password):
    """Creates a new admin user with a 2FA secret key."""
    conn = get_db_connection()
    cur = conn.cursor()

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    otp_secret = pyotp.random_base32()  # Generate 2FA secret key
    
    query = "INSERT INTO users (username, password_hash, otp_secret) VALUES (%s, %s, %s) RETURNING otp_secret;"
    cur.execute(query, (username, password_hash, otp_secret))
    conn.commit()

    otp_secret_key = cur.fetchone()[0]
    
    cur.close()
    conn.close()

    print("User created successfully!")
    print("Use this secret in Google Authenticator:", otp_secret_key)

	•	When a new user is created, it will generate a 2FA secret key.

4. Generate QR Code for Google Authenticator (auth.py)

import pyotp
import qrcode
from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, flash
from database import verify_user, get_db_connection

auth_bp = Blueprint("auth", __name__)

def get_otp_secret(username):
    """Retrieve user's 2FA secret from the database."""
    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT otp_secret FROM users WHERE username = %s;"
    cur.execute(query, (username,))
    otp_secret = cur.fetchone()

    cur.close()
    conn.close()

    return otp_secret[0] if otp_secret else None

def generate_qr_code(username, otp_secret):
    """Generates a QR code for Google Authenticator."""
    otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(
        name=username, issuer_name="Las Vegas AI Admin"
    )
    
    qr = qrcode.make(otp_uri)
    qr.save(f"static/qrcodes/{username}.png")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handles user login with 2FA."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if verify_user(username, password):
            session["username"] = username
            return redirect(url_for("auth.otp_verification"))
        else:
            flash("Invalid credentials.", "danger")

    return render_template("login.html")

@auth_bp.route("/otp", methods=["GET", "POST"])
def otp_verification():
    """Handles 2FA OTP verification."""
    if "username" not in session:
        return redirect(url_for("auth.login"))

    username = session["username"]
    otp_secret = get_otp_secret(username)

    if not otp_secret:
        flash("2FA Secret not found. Contact admin.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        otp_code = request.form["otp"]
        totp = pyotp.TOTP(otp_secret)

        if totp.verify(otp_code):
            session["authenticated"] = True
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid OTP code. Try again.", "danger")

    generate_qr_code(username, otp_secret)  # Generate QR Code for new users

    return render_template("otp.html", username=username)

5. Create OTP Verification Template

templates/otp.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Two-Factor Authentication</title>
</head>
<body>
    <h2>Enter 2FA Code</h2>
    <p>Scan this QR code in Google Authenticator if you haven't already:</p>
    <img src="{{ url_for('static', filename='qrcodes/' + username + '.png') }}" alt="QR Code">
    
    <form method="POST">
        <label>Authentication Code:</label>
        <input type="text" name="otp" required>
        <button type="submit">Verify</button>
    </form>
</body>
</html>

6. Modify dashboard.html to Show Logout Option

Modify dashboard.html to only allow authenticated users.

{% if session['authenticated'] %}
    <p><a href="{{ url_for('auth.logout') }}">Logout</a></p>
{% endif %}

7. Update main.py to Require 2FA for Dashboard

from flask import Flask, render_template, session, redirect, url_for
from database import get_db_connection
from auth import auth_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"  
app.register_blueprint(auth_bp)

def is_logged_in():
    return session.get("authenticated", False)

@app.route("/")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT timestamp, level, source, message FROM logs ORDER BY timestamp DESC LIMIT 50;")
    logs = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("dashboard.html", logs=logs)

8. Updating Docker

Modify Dockerfile to include the new dependencies:

RUN pip install --no-cache-dir flask flask-login flask-bcrypt psycopg2 pyotp qrcode[pil]

Rebuild the Docker image:

docker-compose up --build -d

9. Testing

1️⃣ Register a New Admin

from database import create_user

username = input("Enter username: ")
password = input("Enter password: ")

create_user(username, password)

	•	This will generate a unique 2FA secret.

2️⃣ Login to Dashboard
	1.	Go to http://localhost:5000/login
	2.	Enter username & password.
	3.	Enter the 6-digit OTP code from Google Authenticator.

10. Summary of Security Features

✅ Admin authentication (Username & Password)
✅ Password hashing (bcrypt)
✅ Two-Factor Authentication (TOTP-based)
✅ Session-based login management
✅ QR code for easy Google Authenticator setup

Next Steps

Would you like role-based access control (RBAC) so different users have different permissions (e.g., Viewer vs. Admin)?

Project Overview: AI-Powered Las Vegas Recommendation & Logging System

📌 Project Summary

This project is a web-based AI-driven Las Vegas recommendation system that:
	•	Fetches Las Vegas attractions, restaurants, events, and nightlife data via APIs and web scraping.
	•	Logs API fetch errors, scrapers getting blocked, and system issues.
	•	Provides an admin dashboard for monitoring logs and reviewing system performance.
	•	Implements secure admin authentication with Two-Factor Authentication (2FA) using Google Authenticator.
	•	Uses Docker for containerized deployment and Nginx for production hosting.

📂 Project Structure

las_vegas_ai/
│── docker-compose.yml       # Docker configuration for the app & database
│── Dockerfile               # Defines the Flask app container
│── requirements.txt         # Python dependencies
│── scheduled_tasks.py       # Periodic tasks (API fetch, scraping, log summaries)
│── logs/                    # Stores log files for additional backups
│── static/
│   ├── qrcodes/             # Stores QR codes for 2FA
│── templates/               # HTML templates for Flask views
│   ├── login.html           # Admin login page
│   ├── otp.html             # 2FA verification page
│   ├── dashboard.html       # Admin log dashboard
│── app/                     # Core application
│   ├── main.py              # Flask app (Dashboard)
│   ├── auth.py              # Admin authentication (Login, Logout, 2FA)
│   ├── fetcher.py           # API fetching logic
│   ├── scraper.py           # Web scraping logic
│   ├── alerts.py            # Logging & Alert system
│   ├── database.py          # PostgreSQL connection & user authentication

📜 Key Features & Functionalities

1️⃣ AI-Powered Recommendations

🔹 Data Collection
	•	APIs Used:
	•	Google Places (For attractions, restaurants)
	•	Yelp (For reviews & ratings)
	•	Eventbrite (For concerts & events)
	•	Web Scraping:
	•	Local tourism sites (Trending places, nightlife)
	•	Reddit threads (User-recommended spots)
	•	Categorization:
	•	Food & Drink: Restaurants, bars, cafes
	•	Nightlife: Clubs, lounges, rooftop bars
	•	Outdoor & Adventure: Hiking, skydiving, scenic spots
	•	Events: Concerts, sports, festivals
	•	Hidden Gems: Lesser-known, highly rated places

🔹 File: fetcher.py
	•	Fetches data via APIs
	•	Implements rate limiting and retry mechanisms
	•	Logs API failures, timeouts, and bans in the database

def fetch_data(api_url):
    for attempt in range(3):
        try:
            response = requests.get(api_url, headers=headers, timeout=5)
            if response.status_code == 200:
                log_event("INFO", "API Fetch", f"Successful request to {api_url}")
                return response.json()
            log_event("ERROR", "API Fetch", f"Error {response.status_code}", response.status_code)
            time.sleep(2 ** attempt)  # Exponential backoff
        except requests.RequestException as e:
            log_event("ERROR", "API Fetch", f"Network error: {e}")
    log_event("CRITICAL", "API Fetch", "Max retries reached.")
    return None

2️⃣ Logging System & Alerts

🔹 Logging Levels
	•	INFO: Successful API requests, scrapes, or system operations
	•	WARNING: Minor errors, slow response times
	•	ERROR: API failures, data inconsistencies
	•	CRITICAL: API blocks, scraper bans, server crashes

🔹 File: alerts.py

Handles real-time alerts for critical failures via email notifications.

def send_instant_alert(level, source, message):
    """Sends an immediate email alert for CRITICAL errors."""
    msg = MIMEText(f"🚨 {level} ALERT: {source} 🚨\n\n{message}")
    msg["Subject"] = f"URGENT: {source} Issue Detected"
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(EMAIL_RECEIVERS)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVERS, msg.as_string())
    server.quit()

🔹 File: scheduled_tasks.py
	•	Runs hourly to collect API data & scrape websites.
	•	Sends hourly summary reports via email.

schedule.every(1).hours.do(fetch_api_data)
schedule.every(6).hours.do(scrape_web_data)
schedule.every(1).hours.do(generate_hourly_summary)

3️⃣ Secure Admin Dashboard

🔹 User Authentication
	•	Username & Password Login
	•	Password Hashing (bcrypt)
	•	Two-Factor Authentication (2FA) via Google Authenticator

🔹 File: auth.py

Handles admin login, logout, and 2FA.

@auth_bp.route("/otp", methods=["GET", "POST"])
def otp_verification():
    """Handles 2FA OTP verification."""
    if "username" not in session:
        return redirect(url_for("auth.login"))

    username = session["username"]
    otp_secret = get_otp_secret(username)

    if request.method == "POST":
        otp_code = request.form["otp"]
        totp = pyotp.TOTP(otp_secret)

        if totp.verify(otp_code):
            session["authenticated"] = True
            return redirect(url_for("dashboard"))
        flash("Invalid OTP code. Try again.", "danger")

    return render_template("otp.html", username=username)

🔹 File: dashboard.html
	•	Displays log records.
	•	Admin-only access via login session.
	•	Option to view and resolve errors.

{% if session['authenticated'] %}
    <p><a href="{{ url_for('auth.logout') }}">Logout</a></p>
{% endif %}

4️⃣ Deployment & Hosting

🔹 Dockerized Setup
	•	PostgreSQL for persistent storage.
	•	Flask API for log dashboard.
	•	Cron Jobs for background tasks.

🔹 docker-compose.yml

version: "3.8"

services:
  db:
    image: postgres:latest
    container_name: las_vegas_db
    restart: always
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: las_vegas_db
    ports:
      - "5432:5432"

  flask_app:
    build: .
    container_name: las_vegas_flask
    restart: always
    depends_on:
      - db
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: "postgresql://myuser:mypassword@db/las_vegas_db"

  cron_jobs:
    build: .
    container_name: cron_jobs
    restart: always
    depends_on:
      - db
    command: ["python", "scheduled_tasks.py"]

🔹 Deploying on AWS/DigitalOcean

docker-compose up --build -d

🔹 Nginx Reverse Proxy

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

✅ Final Features Checklist

✔ AI-powered recommendations
✔ Logging & monitoring system
✔ Admin dashboard with 2FA authentication
✔ Email alerts for critical failures
✔ Dockerized deployment

🔜 Next Steps

Would you like to integrate user behavior tracking (e.g., which recommendations they view) to further personalize AI suggestions?

🔹 Enhancing AI with Machine Learning (ML) & User Feedback System

To further personalize recommendations, we’ll:
	1.	Implement ML models to predict user preferences.
	2.	Allow users to provide feedback (👍 Like / 👎 Dislike / 🔍 Want to see more).
	3.	Retrain the AI model periodically to improve accuracy.

📂 Updated Project Structure

las_vegas_ai/
│── ml_model.py              # Machine Learning Model for Recommendation
│── feedback.py              # User Feedback System
│── tracking.py              # User Behavior Tracking (Updated)
│── recommendations.py        # AI Recommendation Engine (Updated)
│── templates/
│   ├── recommendations.html  # Updated for User Feedback
│   ├── feedback.html         # View feedback history

📌 New Features

1️⃣ ML-Powered Personalized Recommendations

We’ll use a collaborative filtering model to predict recommendations based on:
	•	Past user clicks
	•	Explicit feedback (likes/dislikes)
	•	Similar users’ preferences

🔹 File: ml_model.py

import pandas as pd
import psycopg2
from surprise import SVD, Dataset, Reader
from database import get_db_connection

def fetch_user_data():
    """Fetches user interactions and feedback for training the ML model."""
    conn = get_db_connection()
    query = """
        SELECT user_id, recommendation_id, 
               CASE 
                   WHEN action = 'liked' THEN 5 
                   WHEN action = 'disliked' THEN 1 
                   ELSE 3 
               END as rating
        FROM user_interactions;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def train_ml_model():
    """Trains a collaborative filtering model for recommendations."""
    df = fetch_user_data()
    
    if df.empty:
        print("No data available for training.")
        return None

    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_id', 'recommendation_id', 'rating']], reader)
    trainset = data.build_full_trainset()
    
    model = SVD()
    model.fit(trainset)

    return model

def get_ml_recommendations(user_id, model, top_n=5):
    """Generates AI recommendations using ML predictions."""
    df = fetch_user_data()
    
    unique_recs = df['recommendation_id'].unique()
    predictions = [(rec, model.predict(user_id, rec).est) for rec in unique_recs]
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    return [rec[0] for rec in predictions[:top_n]]

# Train model at startup
ml_model = train_ml_model()

2️⃣ Integrate ML into AI Recommendations

🔹 File: recommendations.py (Updated)

from ml_model import get_ml_recommendations, ml_model

def get_personalized_recommendations(user_id):
    """Combines ML predictions with user feedback to personalize recommendations."""
    if ml_model:
        return get_ml_recommendations(user_id, ml_model)
    else:
        return get_default_recommendations()

3️⃣ User Feedback System

Users can like, dislike, or request more similar recommendations.

🔹 PostgreSQL Table for Feedback

CREATE TABLE user_feedback (
    id SERIAL PRIMARY KEY,
    user_id UUID,
    recommendation_id UUID,
    feedback_type VARCHAR(20) CHECK (feedback_type IN ('liked', 'disliked', 'want_more')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

🔹 File: feedback.py

import psycopg2
from database import get_db_connection

def submit_feedback(user_id, recommendation_id, feedback_type):
    """Stores user feedback in the database."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = """INSERT INTO user_feedback (user_id, recommendation_id, feedback_type)
               VALUES (%s, %s, %s);"""
    cur.execute(query, (user_id, recommendation_id, feedback_type))
    
    conn.commit()
    cur.close()
    conn.close()

# Example usage:
# submit_feedback("user123", "rec456", "liked")

4️⃣ Update Frontend to Capture Feedback

🔹 HTML: templates/recommendations.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Recommendations</title>
</head>
<body>
    <h1>Your AI-Powered Las Vegas Recommendations</h1>
    <ul>
        {% for rec in recommendations %}
            <li>
                <h3>{{ rec.name }}</h3>
                <p>Category: {{ rec.category }}</p>
                <button onclick="submitFeedback('{{ rec.id }}', 'liked')">👍 Like</button>
                <button onclick="submitFeedback('{{ rec.id }}', 'disliked')">👎 Dislike</button>
                <button onclick="submitFeedback('{{ rec.id }}', 'want_more')">🔍 Show More</button>
            </li>
        {% endfor %}
    </ul>

    <script>
        function submitFeedback(recId, feedbackType) {
            fetch(`/feedback?rec_id=${recId}&feedback_type=${feedbackType}`)
                .then(response => console.log("Feedback submitted"));
        }
    </script>
</body>
</html>

5️⃣ API Endpoint for Submitting Feedback

🔹 File: feedback.py

from flask import request

@app.route("/feedback")
def feedback():
    """API endpoint for user feedback."""
    if "user_id" not in session:
        return {"error": "Not logged in"}, 403

    user_id = session["user_id"]
    recommendation_id = request.args.get("rec_id")
    feedback_type = request.args.get("feedback_type")

    submit_feedback(user_id, recommendation_id, feedback_type)

    return {"success": True}

6️⃣ View User Feedback History

🔹 File: feedback.py (New Route)

@app.route("/feedback-history")
def feedback_history():
    """Shows the user their feedback history."""
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    conn = get_db_connection()
    cur = conn.cursor()

    query = """SELECT r.name, f.feedback_type, f.timestamp 
               FROM user_feedback f
               JOIN recommendations r ON f.recommendation_id = r.id
               WHERE f.user_id = %s
               ORDER BY f.timestamp DESC;"""
    cur.execute(query, (user_id,))
    feedback_data = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("feedback.html", feedback=feedback_data)

🔹 HTML: templates/feedback.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Your Feedback</title>
</head>
<body>
    <h1>Your Feedback History</h1>
    <ul>
        {% for item in feedback %}
            <li>
                <strong>{{ item[0] }}</strong> - {{ item[1] }} ({{ item[2] }})
            </li>
        {% endfor %}
    </ul>
</body>
</html>

7️⃣ Automate ML Model Retraining

We’ll retrain the model every day to improve its accuracy.

🔹 Update scheduled_tasks.py

import schedule
from ml_model import train_ml_model

def retrain_model():
    global ml_model
    ml_model = train_ml_model()
    print("ML Model retrained!")

schedule.every(24).hours.do(retrain_model)

8️⃣ Docker Deployment Updates

Modify Dockerfile to include ML dependencies:

RUN pip install flask psycopg2 pandas surprise

Rebuild & deploy:

docker-compose up --build -d

✅ Summary of New Features

✔ Machine Learning-powered recommendations
✔ User feedback system (Like, Dislike, Show More)
✔ AI dynamically improves based on interactions
✔ Feedback history page
✔ Automated ML model retraining

🔜 Next Steps

Would you like to add location-based recommendations (e.g., “Near You” suggestions using GPS)? 🌍

📌 Expanded AI System: Adding a Conversational Chatbot & Location-Based Features

To make the Las Vegas AI platform more interactive and useful, we’ll add:
	1.	💬 Conversational Chatbot that:
	•	Recommends places dynamically.
	•	Understands natural language queries.
	•	Uses AI (GPT-based) to answer questions.
	•	Logs interactions for improved personalization.
	2.	📍 Location-Based Recommendations:
	•	Suggests nearby attractions & restaurants based on user location.
	•	Uses Google Maps API for distance-based filtering.
	•	Dynamically updates based on travel history.
	3.	📅 Smart Booking & Itinerary Planning (Future Agent Features):
	•	Users can book events, reserve tables, and add to Google Calendar.
	•	AI automates bookings based on preferences.
	•	Generates a custom travel itinerary.
	•	Connects to Google Calendar API for seamless scheduling.

📂 Updated Project Structure

las_vegas_ai/
│── chatbot.py              # Conversational AI Chatbot
│── location.py             # Location-Based Filtering
│── booking.py              # Booking & Itinerary System
│── templates/
│   ├── chatbot.html        # Chat UI
│   ├── itinerary.html      # Travel Planner
│   ├── recommendations.html # Updated for Location Filtering

1️⃣ Conversational AI Chatbot

Users can chat with an AI assistant that:
	•	Suggests places dynamically.
	•	Answers travel-related questions.
	•	Logs interactions for better recommendations.

🔹 File: chatbot.py

import openai
from flask import request, jsonify, session
from database import get_db_connection

openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_response(user_id, message):
    """Uses GPT to generate a conversational response."""
    prompt = f"User: {message}\nAI:"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    reply = response["choices"][0]["message"]["content"]
    log_chat_history(user_id, message, reply)
    return reply

def log_chat_history(user_id, message, reply):
    """Logs chat messages in the database."""
    conn = get_db_connection()
    cur = conn.cursor()

    query = """INSERT INTO chat_history (user_id, user_message, ai_response) 
               VALUES (%s, %s, %s);"""
    cur.execute(query, (user_id, message, reply))
    
    conn.commit()
    cur.close()
    conn.close()

@app.route("/chat", methods=["POST"])
def chat():
    """API endpoint to chat with the AI assistant."""
    if "user_id" not in session:
        return jsonify({"error": "User not logged in"}), 403

    user_id = session["user_id"]
    message = request.json.get("message")
    reply = generate_response(user_id, message)
    
    return jsonify({"response": reply})

🔹 HTML: templates/chatbot.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chat with AI</title>
</head>
<body>
    <h1>Las Vegas AI Chat Assistant</h1>
    <div id="chatbox"></div>
    
    <input type="text" id="messageInput" placeholder="Ask something...">
    <button onclick="sendMessage()">Send</button>

    <script>
        function sendMessage() {
            const message = document.getElementById("messageInput").value;
            fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("chatbox").innerHTML += 
                    `<p>User: ${message}</p><p>AI: ${data.response}</p>`;
            });
        }
    </script>
</body>
</html>

2️⃣ Location-Based Recommendations

Users can get recommendations near them.

🔹 File: location.py

import requests
from flask import request, session
from database import get_db_connection

GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

def get_user_location():
    """Gets user's coordinates based on IP address."""
    ip = request.remote_addr
    response = requests.get(f"https://ipinfo.io/{ip}/json").json()
    return response.get("loc", "36.1699,-115.1398")  # Default: Las Vegas

def get_nearby_recommendations(user_id):
    """Fetches recommendations near the user's location."""
    lat, lon = get_user_location().split(",")
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT name, category, lat, lon, 
               (3959 * acos(cos(radians(%s)) * cos(radians(lat)) 
               * cos(radians(lon) - radians(%s)) + sin(radians(%s)) 
               * sin(radians(lat)))) AS distance
        FROM recommendations
        HAVING distance < 10
        ORDER BY distance ASC;
    """
    cur.execute(query, (lat, lon, lat))
    results = cur.fetchall()

    cur.close()
    conn.close()
    return results

🔹 Update recommendations.html

<button onclick="getNearby()">Find Nearby</button>
<ul id="nearbyList"></ul>

<script>
    function getNearby() {
        fetch("/recommendations/nearby")
        .then(response => response.json())
        .then(data => {
            document.getElementById("nearbyList").innerHTML = data.map(place => 
                `<li>${place.name} - ${place.distance.toFixed(1)} miles</li>`
            ).join("");
        });
    }
</script>

3️⃣ Booking & Itinerary Planning

Users can book restaurants, shows, or attractions and add to their itinerary.

🔹 File: booking.py

import googleapiclient.discovery
from flask import request, session

GOOGLE_CALENDAR_API_KEY = "YOUR_GOOGLE_CALENDAR_API_KEY"

def add_to_calendar(user_id, event_name, start_time, location):
    """Adds an event to the user's Google Calendar."""
    service = googleapiclient.discovery.build('calendar', 'v3', developerKey=GOOGLE_CALENDAR_API_KEY)
    
    event = {
        'summary': event_name,
        'location': location,
        'start': {'dateTime': start_time, 'timeZone': 'America/Los_Angeles'},
        'end': {'dateTime': start_time, 'timeZone': 'America/Los_Angeles'}
    }
    
    service.events().insert(calendarId='primary', body=event).execute()

@app.route("/book", methods=["POST"])
def book():
    """Handles booking requests."""
    user_id = session["user_id"]
    data = request.json
    add_to_calendar(user_id, data["event"], data["time"], data["location"])
    return {"success": True}

🔹 HTML: templates/itinerary.html

<h1>Your Itinerary</h1>
<ul id="itineraryList"></ul>

<script>
    function addToItinerary(event, time, location) {
        fetch("/book", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ event, time, location })
        }).then(() => alert("Added to itinerary!"));
    }
</script>

✅ Final Features Checklist

✔ Conversational Chatbot (AI Assistant)
✔ Location-Based Recommendations (GPS-based suggestions)
✔ Smart Booking & Google Calendar Integration
✔ Travel Itinerary Generation

🔜 Next Steps

Would you like to add voice interaction (users can talk to the chatbot via speech-to-text)? 🎙️