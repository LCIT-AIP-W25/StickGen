# ✅ FIXED newsapi_scraper.py with pagination and topic limit
from newsapi import NewsApiClient
import pandas as pd
from datetime import datetime
import os
import logging
import time
from bs4 import BeautifulSoup
import requests

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
        queries = [
            "technology", "world", "business", "ai", "science", "climate change",
            "finance", "sports", "cryptocurrency", "innovation"
        ]

        print("🔍 Starting NewsAPI scraping...")
        all_articles = []

        for query in queries:
            for page in range(1, 6):  # Pages 1 to 5
                print(f"🔍 Fetching '{query}', page {page}")
                try:
                    response = newsapi.get_everything(
                        q=query,
                        language='en',
                        sort_by='publishedAt',
                        page=page,
                        page_size=20
                    )
                    articles = response.get('articles', [])
                    for a in articles:
                        try:
                            article_resp = requests.get(a['url'], timeout=5)
                            soup = BeautifulSoup(article_resp.text, "html.parser")
                            paragraphs = soup.find_all("p")
                            full_summary = " ".join(p.get_text() for p in paragraphs[:5]).strip().replace('\n', ' ')
                            if len(full_summary) < 200:
                                full_summary = a['description'] or "No summary available"
                        except:
                            full_summary = a['description'] or "No summary available"

                        all_articles.append({
                            'timestamp': a.get('publishedAt', datetime.now().isoformat()),
                            'title': a.get('title', 'No title'),
                            'summary': full_summary,
                            'link': a.get('url', ''),
                            'source': 'newsapi'
                        })
                    time.sleep(1)
                except Exception as e:
                    logging.warning(f"⚠️ Failed to fetch '{query}' page {page}: {e}")
                    break

        if all_articles:
            df = pd.DataFrame(all_articles).drop_duplicates(subset=["title"])
            filename = f"data/temp_sources/newsapi_{datetime.now().date()}.csv"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            df.to_csv(filename, index=False)
            print(f"✅ NewsAPI records collected: {len(df)}")
            logging.info("✅ NewsAPI collected %d unique articles", len(df))
        else:
            print("⚠️ No NewsAPI articles collected.")

    except Exception as e:
        logging.error("❌ NewsAPI scraping failed: %s", str(e))
        print("❌ Error:", str(e))
