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
                full_url = f"https://www.bbc.com{href}"

                try:
                    article_resp = requests.get(full_url, headers=headers, timeout=5)
                    article_soup = BeautifulSoup(article_resp.text, "html.parser")
                    paragraphs = article_soup.find_all("p")
                    summary_text = " ".join(p.get_text() for p in paragraphs[:3])  # first 3 paragraphs
                except Exception as fetch_error:
                    logging.warning(f"⚠️ Could not fetch full article: {full_url}, error: {fetch_error}")
                    summary_text = text

                headlines.append({
                    "timestamp": datetime.now().isoformat(),
                    "title": text,
                    "summary": summary_text if summary_text else text,
                    "link": full_url,
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
