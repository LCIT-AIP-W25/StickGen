from newsapi import NewsApiClient
import pandas as pd
from datetime import datetime
import os
import logging

log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_folder, "scraping.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def scrape_to_csv():
    try:
        newsapi = NewsApiClient(api_key='3c5d328a803b44c78e084511cb340611')
        articles = newsapi.get_top_headlines(language='en', page_size=50)

        records = []
        for a in articles.get('articles', []):
            records.append({
                'timestamp': a['publishedAt'] or datetime.now().isoformat(),
                'title': a['title'],
                'summary': a['description'],
                'link': a['url'],
                'source': 'newsapi'
            })

        if records:
            filename = f"data/temp_sources/newsapi_{datetime.now().date()}.csv"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            pd.DataFrame(records).drop_duplicates().to_csv(filename, index=False)
            print("✅ NewsAPI records collected:", len(records))
        else:
            print("⚠️ No NewsAPI records found.")

    except Exception as e:
        logging.error("❌ NewsAPI scraping failed: %s", str(e))
        print("❌ Error:", str(e))
