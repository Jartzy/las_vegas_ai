from bs4 import BeautifulSoup
import requests
import random
from alerts import log_event

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

def scrape_page(url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        response = requests.get(url, headers=headers)
        
        if "captcha" in response.text.lower():
            log_event("CRITICAL", "Scraper", "Captcha detected!")
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        log_event("INFO", "Scraper", f"Scraped {url} successfully.")
        return soup
    
    except Exception as e:
        log_event("ERROR", "Scraper", f"Failed to scrape {url}: {e}")
        return None