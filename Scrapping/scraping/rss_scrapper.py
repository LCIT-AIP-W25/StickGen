import feedparser
import csv
import os
from datetime import datetime
import requests
from io import BytesIO

def scrape_to_csv():
    feeds = [
        'http://feeds.bbci.co.uk/news/rss.xml',
        'https://rss.cbc.ca/lineup/topstories.xml'
    ]

    records = []

    for url in feeds:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            feed = feedparser.parse(BytesIO(response.content))
            for entry in feed.entries:
                records.append({
                    "timestamp": entry.published if "published" in entry else datetime.now().isoformat(),
                    "title": entry.title.strip(),
                    "summary": entry.title.strip()[:150] + "...",
                    "link": entry.link.strip(),
                    "source": "bbc_cbc_rss"
                })
        except Exception as e:
            print(f"❌ Failed to fetch from {url}: {e}")

    filename = f"data/temp_sources/rss_combined_{datetime.now().date()}.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "title", "summary", "link", "source"])
        writer.writeheader()
        writer.writerows(records)

    print(f"✅ BBC + CBC RSS collected: {len(records)}")
