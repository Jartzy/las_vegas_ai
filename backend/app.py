# Project Directory Structure
# las_vegas_ai/
# ├── backend/  # Flask API
# │   ├── app.py  # Main Flask application
# │   ├── auth.py  # Authentication routes
# │   ├── recommendations.py  # AI Recommendations
# │   ├── database.py  # Database connection
# │   ├── requirements.txt  # Dependencies
# ├── frontend/  # React App
# │   ├── src/
# │   │   ├── components/
# │   │   ├── pages/
# │   │   ├── api/
# │   │   │   ├── auth.ts  # Handles authentication requests
# │   │   │   ├── recommendations.ts  # Fetches recommendations
# │   │   ├── App.tsx  # Main app
# │   ├── package.json
# ├── docker-compose.yml  # Deployment config
# ├── README.md  # Documentation

from flask import Flask, request, jsonify, session
from flask_cors import CORS
import psycopg2
import bcrypt
import pyotp

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change in production
CORS(app, supports_credentials=True)

DATABASE_URL = "postgresql://myuser:mypassword@db/las_vegas_db"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    otp_code = data.get("otp")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, password_hash, otp_secret FROM users WHERE username = %s;", (username,))
    user = cur.fetchone()
    
    if user:
        user_id, password_hash, otp_secret = user
        
        if bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
            totp = pyotp.TOTP(otp_secret)
            if totp.verify(otp_code):
                session["authenticated"] = True
                session["user_id"] = user_id
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
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, name, category FROM recommendations ORDER BY created_at DESC LIMIT 10;")
    results = cur.fetchall()
    
    cur.close()
    conn.close()
    
    recommendations = [{"id": row[0], "name": row[1], "category": row[2]} for row in results]
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
