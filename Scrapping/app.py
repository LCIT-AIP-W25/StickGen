<<<<<<< HEAD
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
=======
import os
import logging
from flask import Flask

app = Flask(__name__)

>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_folder, "scraping.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

<<<<<<< HEAD
=======
from scraping.bbc_scraper import scrape_to_csv as scrape_bbc
from scraping.newsapi_scraper import scrape_to_csv as scrape_newsapi
from scraping.reddit_scraper import scrape_to_csv as scrape_reddit
from scraping.google_news_scraper import scrape_google_news as scrape_google
from scraping.rss_scrapper import scrape_to_csv as scrape_rss_combined
from pipeline.merge_csv import merge_all_csvs

>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
@app.route('/')
def home():
    return "🚀 News2Buzz Flask app is running!"

@app.route('/run_all_scraping')
def run_all_scraping():
    try:
<<<<<<< HEAD
        logging.info("🔄 Starting all scrapers")
        scrape_bbc()
        scrape_newsapi()
        scrape_reddit()  # ✔️ now uses working snscrape version
        scrape_google()
        scrape_indianexpress()
=======
        if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
            print("⚠️ Avoided duplicate scraping due to Flask reloader.")
            return "⚠️ Duplicate run avoided."

        logging.info("🔄 Starting all scrapers")
        scrape_bbc()
        scrape_newsapi()
        scrape_reddit()
        scrape_google()
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
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
