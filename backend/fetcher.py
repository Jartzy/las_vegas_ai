import requests
import time
from database import get_db_connection
from alerts import log_event

API_KEYS = ["API_KEY_1", "API_KEY_2"]
API_INDEX = 0

def fetch_data(api_url):
    global API_INDEX
    headers = {"Authorization": f"Bearer {API_KEYS[API_INDEX]}"}

    for attempt in range(3):
        try:
            response = requests.get(api_url, headers=headers, timeout=5)

            if response.status_code == 403:
                log_event("CRITICAL", "API Blocked", "403 Forbidden")
                API_INDEX = (API_INDEX + 1) % len(API_KEYS)
                time.sleep(60)

            if response.status_code == 200:
                log_event("INFO", "API Fetch", f"Successful request to {api_url}")
                return response.json()

            log_event("ERROR", "API Fetch", f"Error {response.status_code}", response.status_code)
            time.sleep(2 ** attempt)

        except requests.RequestException as e:
            log_event("ERROR", "API Fetch", f"Network error: {e}")

    log_event("CRITICAL", "API Fetch", "Max retries reached.")
    return None