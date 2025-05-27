import praw
import pandas as pd
from datetime import datetime
import os
import logging

import praw

reddit = praw.Reddit(
    client_id="hiyvj6zGXkLqMJFvMlfb1Q",
    client_secret="ZA9VTZ6i-QyXzwCRfUuhran4Ojr_Vw",
    user_agent="Mozilla/5.0 (News2Buzz bot by u/Top-Touch2323)"
)


log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_folder, "scraping.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def scrape_to_csv():
    try:
        records = []
        for post in reddit.subreddit('all').new(limit=100):
            summary = post.selftext[:250] if post.selftext else post.title
            records.append({
                'timestamp': datetime.utcfromtimestamp(post.created_utc).isoformat(),
                'title': post.title,
                'summary': summary,
                'link': post.url,
                'source': 'reddit'
            })

        filename = f"data/temp_sources/reddit_{datetime.now().date()}.csv"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        pd.DataFrame(records).to_csv(filename, index=False)
        print("✅ Reddit records collected:", len(records))

    except Exception as e:
        print("❌ Reddit scraping failed:", str(e))
        logging.error("❌ Reddit scraping failed: %s", str(e))
