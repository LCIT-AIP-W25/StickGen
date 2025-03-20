import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Constants
CATEGORY_URL = "https://indianexpress.com/section/world/"
OUTPUT_FILE = "World_data1.csv"
TIMEOUT = 180  # Page load timeout in seconds
INTERVAL = 300  # Scrape every 5 minutes

# Function to initialize the Chrome driver
def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(TIMEOUT)
    return driver

# Function to read previously scraped URLs
def get_scraped_urls(output_file):
    if os.path.exists(output_file):
        df = pd.read_csv(output_file)
        return set(df['url'].dropna())
    return set()

# Function to scrape articles
def scrape_articles():
    while True:
        driver = setup_driver()
        driver.get(CATEGORY_URL)
        time.sleep(3)
        
        scraped_urls = get_scraped_urls(OUTPUT_FILE)
        scraped_data = []

        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            articles = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.north-east-grid.explained-section-grid ul li a"))
            )
            
            article_links = [article.get_attribute("href") for article in articles]

            new_articles_found = False
            for url in article_links:
                if url in scraped_urls:
                    print("No new articles found. Stopping scrape.")
                    break  # Stop scraping if we hit an already saved article
                
                new_articles_found = True
                try:
                    driver.get(url)
                    time.sleep(5)

                    headline = driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div > h1").text
                    description = driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div > h2").text
                    content = driver.find_element(By.CSS_SELECTOR, "#pcl-full-content").text if driver.find_elements(By.CSS_SELECTOR, "#pcl-full-content") else ""
                    date_element = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="dateModified"]')
                    date_time = date_element.get_attribute("content") if date_element else ""
                    
                    scraped_data.append([headline, description, content, date_time, url])
                    print(f"Scraped: {url}")
                    
                except Exception as e:
                    print(f"Error scraping {url}: {e}")
                    scraped_data.append(["", "", "", "", url])
                
                driver.get(CATEGORY_URL)
                time.sleep(3)
        
        except Exception as e:
            print("Error scraping page:", e)
        
        driver.quit()
        
        if scraped_data:
            df = pd.DataFrame(scraped_data, columns=['headline', 'description', 'content', 'date_time', 'url'])
            df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
            df = df.sort_values(by='date_time', ascending=False)
            df.to_csv(OUTPUT_FILE, mode='a', header=not os.path.exists(OUTPUT_FILE), index=False)
            print(f"Scraping complete. Data saved to {OUTPUT_FILE}")

        if not new_articles_found:
            print("No new articles detected. Waiting for the next cycle.")

        print(f"Waiting {INTERVAL / 60} minutes before next scrape...")
        time.sleep(INTERVAL)

# Run scraping
scrape_articles()
