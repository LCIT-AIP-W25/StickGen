import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import logging

# Logging setup
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_folder, "scraping.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def scrape_to_csv():
    try:
        url = "https://www.bbc.com/news"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        headlines = []

        for link in soup.find_all("a", href=True):
            href = link['href']
            text = link.get_text(strip=True)

            if "/news/" in href and text and len(text.split()) > 4:
                headlines.append({
                    "timestamp": datetime.now().isoformat(),
                    "title": text,
                    "summary": text[:150] + "...",
                    "link": f"https://www.bbc.com{href}",
                    "source": "bbc"
                })

        print(f"Found {len(headlines)} headlines")

        if headlines:
            filename = f"data/temp_sources/bbc_{datetime.now().date()}.csv"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            pd.DataFrame(headlines).drop_duplicates().to_csv(filename, index=False)
            print(f"✅ BBC records collected: {len(headlines)}")
            logging.info("✅ BBC scraped %d records", len(headlines))
        else:
            print("⚠️ No valid headlines found.")
            logging.warning("⚠️ No valid headlines found in BBC scraper.")

    except Exception as e:
        logging.error("❌ BBC scraping failed: %s", str(e))
        print("❌ Error:", str(e))
