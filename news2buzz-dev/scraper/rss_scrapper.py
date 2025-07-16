import snscrape.modules.reddit as reddit
from datetime import datetime
import os
import logging

# Logging
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_folder, "scraping.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def scrape_to_json():
    try:
        print("🔄 Starting Reddit scrape without Pushshift (pure Python)...")
        posts = []

        for i, post in enumerate(reddit.RedditSearchScraper('subreddit:worldnews').get_items()):
            if i >= 50:
                break

            posts.append({
                "timestamp": post.date.isoformat(),
                "title": post.title,
                "summary": post.selftext[:250] if post.selftext else post.title,
                "link": post.url,
                "source": "reddit"
            })

        print(f"✅ Reddit scraping complete: {len(posts)} posts collected.")
        logging.info("✅ Reddit scraping complete: %d posts", len(posts))
        return posts

    except Exception as e:
        print(f"❌ Reddit scraping failed: {e}")
        logging.error("❌ Reddit scraping failed: %s", str(e))
        return []
