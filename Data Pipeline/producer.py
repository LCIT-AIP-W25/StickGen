from kafka import KafkaProducer
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

# Kafka Producer Configuration
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# NewsAPI Configuration
API_KEY = "pub_66788539282e1523ae8f8e779af1e8fcceb36"  # Replace with your NewsAPI key
base_url = "https://newsapi.org/v2/top-headlines"
params = {
    "country": "us",
    "apiKey": API_KEY,
    "pageSize": 100,  # Maximum articles per request
    "from": "2025-01-05T00:00:00",  # Start date (replace with your desired start date)
    "to": "2025-01-14T23:59:59",    # End date (replace with your desired end date)
}

# Static Scraping with BeautifulSoup
def scrape_full_content_static(article_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(article_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = soup.find_all('p')
            full_content = " ".join([para.get_text() for para in paragraphs]).strip()
            return full_content
        else:
            print(f"Failed to fetch content from {article_url}. HTTP Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error in static scraping: {e}")
        return None

# Dynamic Scraping with Selenium
def scrape_full_content_dynamic(article_url):
    try:
        # Set up Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run browser in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering for headless mode
        chrome_options.add_argument("--no-sandbox")
        service = Service("path_to_chromedriver")  # Replace with your ChromeDriver path
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Load the article page
        driver.get(article_url)
        
        # Extract all paragraph text
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        full_content = " ".join([para.text for para in paragraphs])
        
        driver.quit()
        return full_content.strip()
    except Exception as e:
        print(f"Error in dynamic scraping: {e}")
        return None

# Fetch News Articles from NewsAPI and Publish to Kafka
for page in range(1, 6):  # Adjust range to fetch more pages
    params["page"] = page
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        for article in articles:
            # Scrape full content using static method first
            full_content = scrape_full_content_static(article['url'])

            # If static scraping fails, use dynamic scraping with Selenium
            if not full_content:
                full_content = scrape_full_content_dynamic(article['url'])

            # Add full content to the article
            article['full_content'] = full_content if full_content else article.get('content', '')

            # Publish the article to Kafka
            producer.send('news', article)
            print(f"Published to Kafka: {article['title']}")
    else:
        print(f"Failed to fetch news from NewsAPI. HTTP Status: {response.status_code}")
        break

# Close Kafka Producer
producer.close()
