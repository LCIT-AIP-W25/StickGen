<<<<<<< HEAD
=======
# ✅ FIXED newsapi_scraper.py with pagination and topic limit
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
from newsapi import NewsApiClient
import pandas as pd
from datetime import datetime
import os
import logging
import time
<<<<<<< HEAD
import random

# Setup logging
=======
from bs4 import BeautifulSoup
import requests

>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
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
<<<<<<< HEAD

        # Full query list
        full_queries = [
            "technology", "world", "business", "ai", "science", "environment", "climate change", "health",
            "politics", "economy", "finance", "sports", "entertainment", "gaming", "cryptocurrency",
            "blockchain", "innovation", "startups", "education", "travel", "lifestyle", "culture",
            "history", "artificial intelligence", "machine learning", "data science", "cybersecurity",
            "privacy", "social media", "internet of things", "5G", "quantum computing", "augmented reality",
            "virtual reality", "metaverse", "sustainability", "renewable energy", "space exploration", "robotics",
            "automation", "biotechnology", "genomics", "healthcare technology", "digital transformation",
            "cloud computing", "big data", "analytics", "e-commerce", "fintech", "edtech", "proptech"
        ]

        # Randomize and select a limited batch (to avoid hitting 100 req/day or 50 req/12hr)
        max_queries = 20
        random.shuffle(full_queries)
        queries = full_queries[:max_queries]

        print(f"🔍 Starting NewsAPI scraping ({len(queries)} queries)...")
        all_articles = []

        for query in queries:
            try:
                response = newsapi.get_everything(
                    q=query,
                    language='en',
                    sort_by='publishedAt',
                    page_size=50,
                )

                if response.get("status") == "error" and response.get("code") == "rateLimited":
                    print(f"🚫 Rate limit hit while querying '{query}'. Stopping.")
                    logging.warning(f"🚫 Rate limit hit at query '{query}'.")
                    break

                articles = response.get('articles', [])
                for a in articles:
                    all_articles.append({
                        'timestamp': a['publishedAt'] or datetime.now().isoformat(),
                        'title': a['title'],
                        'summary': a['description'] or "No summary available",
                        'link': a['url'],
                        'source': 'newsapi'
                    })

                time.sleep(1)  # polite delay
            except Exception as e:
                logging.warning(f"⚠️ Failed to fetch '{query}': {e}")
                print(f"⚠️ Failed to fetch '{query}': {e}")

        if all_articles:
            df = pd.DataFrame(all_articles).drop_duplicates(subset=["title", "link"])
=======
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
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
            filename = f"data/temp_sources/newsapi_{datetime.now().date()}.csv"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            df.to_csv(filename, index=False)
            print(f"✅ NewsAPI records collected: {len(df)}")
            logging.info("✅ NewsAPI collected %d unique articles", len(df))
        else:
            print("⚠️ No NewsAPI articles collected.")
<<<<<<< HEAD
            logging.warning("⚠️ No NewsAPI articles collected.")
=======
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74

    except Exception as e:
        logging.error("❌ NewsAPI scraping failed: %s", str(e))
        print("❌ Error:", str(e))
<<<<<<< HEAD

if __name__ == "__main__":
    scrape_to_csv()
=======
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
