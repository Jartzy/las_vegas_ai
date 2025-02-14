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