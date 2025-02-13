import psycopg2
import os
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@db/las_vegas_db")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def create_user(username, password):
    """Hashes password and creates a new admin user."""
    conn = get_db_connection()
    cur = conn.cursor()

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    query = "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id;"
    
    try:
        cur.execute(query, (username, password_hash))
        conn.commit()
        print("User created successfully!")
    except Exception as e:
        print(f"Error: {e}")
    
    cur.close()
    conn.close()

def verify_user(username, password):
    """Checks if username exists and verifies password."""
    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT password_hash FROM users WHERE username = %s;"
    cur.execute(query, (username,))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user and bcrypt.check_password_hash(user[0], password):
        return True
    return False