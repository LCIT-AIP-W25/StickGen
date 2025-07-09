import snscrape.modules.reddit as reddit
import pandas as pd
from datetime import datetime
import os
<<<<<<< HEAD
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
        print("🔄 Starting Reddit scrape using snscrape...")
        posts = []

        for i, post in enumerate(reddit.RedditSearchScraper('subreddit:worldnews').get_items()):
            if i >= 100:
=======

def scrape_to_csv():
    try:
        print("🔄 Starting Reddit scrape without Pushshift...")
        posts = []

        for i, post in enumerate(reddit.RedditSearchScraper('subreddit:worldnews').get_items()):
            if i >= 100:  # Limit to 100 posts
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
                break

            posts.append({
                "timestamp": post.date.isoformat(),
<<<<<<< HEAD
                "title": post.title.strip(),
                "summary": post.selftext[:250].strip() if post.selftext else post.title.strip(),
=======
                "title": post.title,
                "summary": post.selftext if post.selftext else post.title,
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
                "link": post.url,
                "source": "reddit"
            })

<<<<<<< HEAD
        if not posts:
            print("⚠️ No posts found from Reddit.")
            logging.warning("⚠️ Reddit scraper returned 0 posts.")
            return

        # Save to CSV
        df = pd.DataFrame(posts).drop_duplicates(subset=["title", "link"])
        os.makedirs("data/temp_sources", exist_ok=True)
        out_file = f"data/temp_sources/reddit_{datetime.now().date()}.csv"
        df.to_csv(out_file, index=False)

        print(f"✅ Reddit scraping complete: {len(df)} posts saved to {out_file}")
        logging.info("✅ Reddit scraped %d posts to %s", len(df), out_file)

    except Exception as e:
        print(f"❌ Reddit scraping failed: {e}")
        logging.error("❌ Reddit scraping failed: %s", str(e))
=======
        os.makedirs("data/temp_sources", exist_ok=True)
        out_file = f"data/temp_sources/reddit_{datetime.now().date()}.csv"
        pd.DataFrame(posts).drop_duplicates(subset=["title", "link"]).to_csv(out_file, index=False)
        print(f"✅ Reddit scraping complete: {len(posts)} posts saved to {out_file}")
    
    except Exception as e:
        print(f"❌ Reddit scraping failed: {e}")
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74

if __name__ == "__main__":
    scrape_to_csv()
