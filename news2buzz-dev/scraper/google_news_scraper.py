# ✅ FIXED google_news_scraper.py with shared driver and error recovery
import os
import time
import logging
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = "data/temp_sources"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "google_news.csv")
TOPICS = ["technology", "business", "ai", "world", "innovation"]

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(options=chrome_options)

def get_summary_from_article(link):
    try:
        article_resp = requests.get(link, timeout=10)
        soup = BeautifulSoup(article_resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        return " ".join(p.get_text() for p in paragraphs[:5]).strip()
    except:
        return ""

def scrape_google_news():
    logging.info("🔍 Starting Google News scraping")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_data = []

    driver = setup_driver()
    for topic in TOPICS:
        try:
            print(f"\n🌐 Loading topic: {topic}")
            url = f"https://news.google.com/search?q={topic}&hl=en-US&gl=US&ceid=US:en"
            driver.get(url)
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "article")))
            time.sleep(2)
            articles = driver.find_elements(By.TAG_NAME, "article")
            print(f"🔍 Found {len(articles)} articles for '{topic}'")
            count = 0
            for article in articles:
                try:
                    a_tags = article.find_elements(By.TAG_NAME, "a")
                    title_elem = max(a_tags, key=lambda a: len(a.text.strip()), default=None)
                    if not title_elem or not title_elem.text.strip():
                        continue
                    title = title_elem.text.strip()
                    link = title_elem.get_attribute("href")
                    if link.startswith("./"):
                        link = "https://news.google.com" + link[1:]
                    summary = get_summary_from_article(link)
                    all_data.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "title": title,
                        "summary": summary or title,
                        "link": link,
                        "source": "google_news",
                        "topic": topic
                    })
                    count += 1
                except Exception as e:
                    print(f"⚠️ Skipping article: {e}")
            print(f"✅ {topic}: {count} collected.")
        except Exception as e:
            print(f"⚠️ Error loading topic '{topic}': {e}")

    driver.quit()
    if all_data:
        df = pd.DataFrame(all_data).drop_duplicates(subset=["title", "link"])
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\n✅ Scraped {len(df)} unique Google News headlines.")
    else:
        print("\n⚠️ No Google News articles scraped.")
