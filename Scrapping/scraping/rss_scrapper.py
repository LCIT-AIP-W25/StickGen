import snscrape.modules.reddit as reddit
import pandas as pd
from datetime import datetime
import os

def scrape_to_csv():
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

        os.makedirs("data/temp_sources", exist_ok=True)
        output_csv = f"data/temp_sources/reddit_{datetime.now().date()}.csv"
        pd.DataFrame(posts).to_csv(output_csv, index=False)
        print(f"✅ Reddit scraping complete: {len(posts)} posts saved to {output_csv}")
    
    except Exception as e:
        print(f"❌ Reddit scraping failed: {e}")
