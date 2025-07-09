import json
import logging
import time
import random
import hashlib
import json
import logging
from kafka import KafkaProducer
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from kafka import KafkaProducer
from webdriver_manager.chrome import ChromeDriverManager

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "news_topic"

# Yahoo News URL
BASE_URL = 'https://ca.news.yahoo.com/'

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    """Sets up a Selenium WebDriver with Chrome."""
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")  # Run headless for efficiency
    options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_yahoo_news():
    """Scrapes Yahoo News articles by scrolling and extracting headlines, links, and descriptions."""
    driver = setup_driver()
    driver.get(BASE_URL)
    time.sleep(3)  # Allow initial page load

    articles = []
    processed_articles = set()  # Track already processed articles
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(5):  # Scroll multiple times to load more news
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        news_items = soup.find_all('li', class_='js-stream-content')

        for item in news_items:
            try:
                headline = item.find('h3').get_text(strip=True) if item.find('h3') else 'No Title'
                link = item.find('a')['href'] if item.find('a') else ''
                description = item.find('p').get_text(strip=True) if item.find('p') else 'No Description'
                full_link = f'https://ca.news.yahoo.com{link}' if link.startswith('/') else link

                # Generate a unique identifier for duplicates (headline + link)
                unique_string = headline + full_link
                unique_hash = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()

                if unique_hash not in processed_articles:  # Ensure no duplicates
                    processed_articles.add(unique_hash)
                    articles.append({
                        'headline': headline,
                        'link': full_link,
                        'short_description': description,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    logging.info(f"Found new article: {headline[:50]}...")
                else:
                    logging.info(f"Duplicate skipped: {headline[:50]}")

            except Exception as e:
                logging.error(f"Error processing an article: {e}")
                continue

        # Scroll down and wait for new content to load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 5))

        # Check if page height changes (stop scrolling if no new content loads)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()
    logging.info(f"Total articles scraped: {len(articles)}")
    return articles

def send_to_kafka(articles):
    """Sends scraped articles to Kafka for processing."""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        for article in articles:
            producer.send(KAFKA_TOPIC, article)
            logging.info(f"Sent article to Kafka: {article['headline'][:50]}...")

        producer.flush()
        producer.close()
        logging.info("Finished sending all articles to Kafka.")

    except Exception as e:
        logging.error(f"Error sending articles to Kafka: {e}")

if __name__ == "__main__":
    articles = scrape_yahoo_news()
    if articles:
        send_to_kafka(articles)
    else:
        logging.info("No articles found. Exiting.")