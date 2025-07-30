from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

CATEGORY_URL = "https://indianexpress.com/section/world/"

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver

def scrape_to_json():
    driver = setup_driver()
    articles = []

    try:
        driver.get(CATEGORY_URL)
        time.sleep(3)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul li a")))
        links = driver.find_elements(By.CSS_SELECTOR, "ul li a")
        urls = [a.get_attribute("href") for a in links if a.get_attribute("href")]

        for url in urls[:10]:
            try:
                driver.get(url)
                headline = driver.find_element(By.CSS_SELECTOR, "h1").text
                summary = driver.find_element(By.CSS_SELECTOR, "#pcl-full-content").text
                articles.append({
                    "timestamp": datetime.now().isoformat(),
                    "title": headline.strip(),
                    "summary": summary.strip(),
                    "link": url,
                    "source": "indianexpress"
                })
            except Exception as e:
                print(f"⚠️ Error scraping {url}: {e}")
    finally:
        driver.quit()

    return articles
