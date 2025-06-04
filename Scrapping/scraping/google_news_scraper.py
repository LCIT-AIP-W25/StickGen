import feedparser
import pandas as pd
import os
from datetime import datetime
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
        feeds = {
            "general": "https://news.google.com/news/rss?hl=en-US&gl=US&ceid=US:en",
            "world": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
            "tech": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en",
            "business": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",
            "science": "https://news.google.com/rss/headlines/section/topic/SCIENCE?hl=en-US&gl=US&ceid=US:en"
        }

        records = []

        for tag, url in feeds.items():
            feed = feedparser.parse(url)
            for entry in feed.entries:
                records.append({
                    "timestamp": entry.published if "published" in entry else datetime.now().isoformat(),
                    "title": entry.title.strip(),
                    "summary": entry.title.strip()[:150] + "...",
                    "link": entry.link.strip(),
                    "source": f"google_news_{tag}"
                })

        if records:
            df = pd.DataFrame(records).drop_duplicates(subset=["title"])
            filename = f"data/temp_sources/google_news_{datetime.now().date()}.csv"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            df.to_csv(filename, index=False)
            print(f"✅ Google News RSS collected: {len(df)} unique records")
            logging.info("✅ Google News RSS collected %d records", len(df))
        else:
            print("⚠️ No Google News articles found.")

    except Exception as e:
        logging.error("❌ Google News RSS scraping failed: %s", str(e))
        print("❌ Error:", str(e))
