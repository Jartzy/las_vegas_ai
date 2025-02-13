import psycopg2
import uuid
from database import get_db_connection

def log_interaction(user_id, recommendation_id, action):
    """Logs user interaction (viewed or clicked)."""
    conn = get_db_connection()
    cur = conn.cursor()

    query = """INSERT INTO user_interactions (user_id, recommendation_id, action)
               VALUES (%s, %s, %s);"""
    cur.execute(query, (user_id, recommendation_id, action))
    
    conn.commit()
    cur.close()
    conn.close()

# Example usage:
# log_interaction("user123", "rec456", "clicked")