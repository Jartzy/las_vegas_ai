import schedule
import time
from fetcher import fetch_data
from scraper import scrape_page
from alerts import generate_hourly_summary

API_URLS = [
    "https://api.example.com/places",
    "https://api.example.com/events"
]

SCRAPE_URLS = [
    "https://www.example.com/trending-places",
    "https://www.example.com/nightlife"
]

def fetch_api_data():
    for url in API_URLS:
        fetch_data(url)

def scrape_web_data():
    for url in SCRAPE_URLS:
        scrape_page(url)

# Scheduling Jobs
schedule.every(1).hours.do(fetch_api_data)
schedule.every(6).hours.do(scrape_web_data)
schedule.every(1).hours.do(generate_hourly_summary)

# Run scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(30)