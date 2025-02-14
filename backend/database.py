import os
import pyotp
import psycopg2
from psycopg2 import OperationalError
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Ensure DATABASE_URL is read correctly
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@las_vegas_db/las_vegas_db")

def get_db_connection():
    """Establishes and returns a PostgreSQL database connection."""
    try:
        print(f"🔹 Connecting to database: {DATABASE_URL}")  # Debugging
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except OperationalError as e:
        print(f"🚨 Database connection failed: {e}")
        return None  # Handle gracefully instead of crashing

def create_user(username, password):
    """Creates a new user with a hashed password & 2FA secret key."""
    conn = get_db_connection()
    if not conn:
        print("🚨 Unable to create user: No database connection.")
        return None

    cur = conn.cursor()
    
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    otp_secret = pyotp.random_base32()  # Generate a 2FA secret key
    
    query = "INSERT INTO users (username, password_hash, otp_secret) VALUES (%s, %s, %s) RETURNING otp_secret;"
    cur.execute(query, (username, password_hash, otp_secret))
    conn.commit()

    otp_secret_key = cur.fetchone()[0]
    
    cur.close()
    conn.close()

    print("✅ User created successfully!")
    print("🔑 Use this secret in Google Authenticator:", otp_secret_key)
    return otp_secret_key  # ✅ Return the secret for debugging

def verify_user(username, password):
    """Verify username and password against stored hashed password."""
    conn = get_db_connection()
    if not conn:
        print("🚨 Unable to verify user: No database connection.")
        return False

    cur = conn.cursor()

    query = "SELECT password_hash FROM users WHERE username = %s;"
    cur.execute(query, (username,))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        print("🔹 Stored Hash:", user[0])  # Debugging
        print("🔹 Checking Password:", password)  # Debugging

        try:
            if bcrypt.check_password_hash(user[0], password):
                print("✅ Password match!")  # Debugging
                return True
            else:
                print("❌ Password mismatch!")  # Debugging
        except ValueError as e:
            print("🚨 Bcrypt Error:", e)  # Debugging
            return False

    return False