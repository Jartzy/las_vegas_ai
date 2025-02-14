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