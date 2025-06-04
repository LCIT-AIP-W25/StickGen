from newsapi import NewsApiClient
import pandas as pd
from datetime import datetime
import os
import logging
import time

# Setup logging
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

        queries = ["technology", "world", "business", "ai", "science","environment", "climate change", "health", "politics", "economy", "finance", "sports", "entertainment", "gaming", "cryptocurrency", "blockchain", "innovation", "startups", "education", "travel", "lifestyle", "culture", "history", "artificial intelligence", "machine learning", "data science", "cybersecurity", "privacy", "social media", "internet of things", "5G", "quantum computing", "augmented reality", "virtual reality", "metaverse", "sustainability", "renewable energy", "space exploration", "robotics", "automation", "biotechnology", "genomics", "healthcare technology", "digital transformation", "cloud computing", "big data", "analytics", "e-commerce", "fintech", "edtech", "proptech"]
        print("🔍 Starting NewsAPI scraping...")
        all_articles = []

        for query in queries:
            print(f"🔍 Fetching news for: {query}")
            try:
                response = newsapi.get_everything(
                    q=query,
                    language='en',
                    sort_by='publishedAt',
                    page_size=50,
                )
                articles = response.get('articles', [])
                for a in articles:
                    all_articles.append({
                        'timestamp': a['publishedAt'] or datetime.now().isoformat(),
                        'title': a['title'],
                        'summary': a['description'] or "No summary available",
                        'link': a['url'],
                        'source': 'newsapi'
                    })

                time.sleep(1)  # polite delay to avoid rate-limiting
            except Exception as e:
                logging.warning(f"⚠️ Failed to fetch '{query}': {e}")
                print(f"⚠️ Failed to fetch '{query}': {e}")

        if all_articles:
            df = pd.DataFrame(all_articles).drop_duplicates(subset=["title"])
            filename = f"data/temp_sources/newsapi_{datetime.now().date()}.csv"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            df.to_csv(filename, index=False)
            print(f"✅ NewsAPI records collected: {len(df)}")
            logging.info("✅ NewsAPI collected %d unique articles", len(df))
        else:
            print("⚠️ No NewsAPI articles collected.")
            logging.warning("⚠️ No NewsAPI articles collected.")

    except Exception as e:
        logging.error("❌ NewsAPI scraping failed: %s", str(e))
        print("❌ Error:", str(e))
