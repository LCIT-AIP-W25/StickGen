from flask import Flask
import logging
import os

# Importing scraper functions (✔️ updated Reddit to use snscrape version)
from scraping.bbc_scraper import scrape_to_csv as scrape_bbc
from scraping.newsapi_scraper import scrape_to_csv as scrape_newsapi
from scraping.reddit_scraper import scrape_to_csv as scrape_reddit
from scraping.google_news_scraper import scrape_to_csv as scrape_google
from scraping.rss_scrapper import scrape_to_csv as scrape_rss_combined
from scraping.indian_express_scraper import scrape_to_csv as scrape_indianexpress
from pipeline.merge_csv import merge_all_csvs

app = Flask(__name__)

# Logging setup
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_folder, "scraping.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route('/')
def home():
    return "🚀 News2Buzz Flask app is running!"

@app.route('/run_all_scraping')
def run_all_scraping():
    try:
        logging.info("🔄 Starting all scrapers")
        scrape_bbc()
        scrape_newsapi()
        scrape_reddit()  # ✔️ now uses working snscrape version
        scrape_google()
        scrape_indianexpress()
        scrape_rss_combined()
        logging.info("✅ All scrapers completed")

        merge_all_csvs()
        logging.info("✅ Merging complete")

        return "✅ Full scraping pipeline complete. Check merged_news.csv"

    except Exception as e:
        logging.error("❌ Error in scraping pipeline", exc_info=True)
        return f"❌ Error during scraping: {e}"

if __name__ == "__main__":
    app.run(debug=True)
