import feedparser
import csv
import os
from datetime import datetime

def scrape_to_csv():
    rss_url = "https://news.google.com/news/rss?hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)

    records = []
    for entry in feed.entries:
        records.append({
            "timestamp": entry.published if "published" in entry else datetime.now().isoformat(),
            "title": entry.title.strip(),
            "summary": entry.summary.strip()[:150] + "...",
            "link": entry.link.strip(),
            "source": "google_news"
        })

    filename = f"data/temp_sources/google_news_{datetime.now().date()}.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "title", "summary", "link", "source"])
        writer.writeheader()
        writer.writerows(records)

    print(f"✅ Google News RSS collected: {len(records)}")
