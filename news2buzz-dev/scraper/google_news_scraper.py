import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def scrape_to_json():
    driver = setup_driver()
    articles = []

    for topic in TOPICS:
        try:
            print(f"\n🌐 Loading topic: {topic}")
            url = f"https://news.google.com/search?q={topic}&hl=en-US&gl=US&ceid=US:en"
            driver.get(url)
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "article")))
            time.sleep(2)
            entries = driver.find_elements(By.TAG_NAME, "article")
            print(f"🔍 Found {len(entries)} articles for '{topic}'")

            for article in entries:
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

                    articles.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "title": title,
                        "summary": summary or title,
                        "link": link,
                        "source": "google_news",
                        "topic": str(topic)
                    })
                except Exception as e:
                    print(f"⚠️ Skipping article: {e}")
        except Exception as e:
            print(f"⚠️ Error loading topic '{topic}': {e}")
    driver.quit()
    return articles
