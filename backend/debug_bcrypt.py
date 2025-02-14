import bcrypt
from database import get_db_connection

# Establish a database connection
conn = get_db_connection()
cur = conn.cursor()

# Fetch stored password hash for "admin"
cur.execute("SELECT password_hash FROM users WHERE username = 'admin';")
user = cur.fetchone()

cur.close()
conn.close()

if user:
    stored_hash = user[0]  # Get the stored bcrypt hash
    print(f"🔹 Stored Hash (Raw): {stored_hash}")
    print(f"🔹 Type: {type(stored_hash)}")

    try:
        # Ensure stored hash is correctly encoded
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.strip().encode('utf-8')
        
        test_password = "securepassword"
        print(f"🔹 Checking Password: {test_password}")

        # Check password
        if bcrypt.checkpw(test_password.encode('utf-8'), stored_hash):
            print("✅ Password matches!")
        else:
            print("❌ Password mismatch!")

    except ValueError as e:
        print(f"🚨 Bcrypt Error: {e}")
else:
    print("🚨 No user found with that username!")
