# backend/ingest_data.py
import os
import requests
from app import app, db, Recommendation
from dotenv import load_dotenv
load_dotenv()  # This loads variables from a .env file in the current directory or in the project root.

def fetch_recommendations():
    api_key = os.environ.get("TICKETMASTER_API_KEY", "YOUR_TICKETMASTER_API_KEY")
    print("Using API key:", api_key)  # Debug: show which API key is used
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={api_key}&city=Las+Vegas"
    print("Requesting URL:", url)
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        events = data.get("_embedded", {}).get("events", [])
        print("Fetched", len(events), "events")  # Debug: show number of events fetched
        
        recommendations = []
        for event in events:
            name = event.get("name")
            classifications = event.get("classifications", [])
            if classifications:
                category = classifications[0].get("segment", {}).get("name", "Event")
            else:
                category = "Event"
            
            recommendations.append({
                "name": name,
                "category": category
            })
        return recommendations
    except requests.exceptions.RequestException as e:
        print("Error fetching Ticketmaster data:", e)
        return []

def ingest_recommendations():
    rec_data = fetch_recommendations()
    if not rec_data:
        print("No recommendations were fetched.")
        return
    
    for item in rec_data:
        recommendation = Recommendation(
            name=item.get("name"),
            category=item.get("category")
        )
        # Avoid duplicates based on event name
        if not Recommendation.query.filter_by(name=recommendation.name).first():
            db.session.add(recommendation)
    
    try:
        db.session.commit()
        print("✅ Ticketmaster events ingested successfully.")
    except Exception as e:
        db.session.rollback()
        print("Error committing recommendations to the database:", e)

if __name__ == "__main__":
    with app.app_context():
        ingest_recommendations()