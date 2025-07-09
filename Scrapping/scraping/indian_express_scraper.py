import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import os
import logging

# Logging
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_folder, "scraping.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

CATEGORY_URL = "https://indianexpress.com/section/world/"
OUTPUT_FILE = f"data/temp_sources/indianexpress_{datetime.now().date()}.csv"
TIMEOUT = 180

def setup_driver():
    chrome_options = webdriver.ChromeOptions()
<<<<<<< HEAD
    chrome_options.add_argument("--headless=new")  # ✅ updated headless mode
=======
    chrome_options.add_argument("--headless=new")  # ✅ use updated headless mode
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
<<<<<<< HEAD
    chrome_options.add_argument("--log-level=3")  # Less verbose output
    chrome_options.add_argument("--enable-unsafe-swiftshader")
=======
    chrome_options.add_argument("--log-level=3")  # Reduce noise
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
<<<<<<< HEAD
    driver.set_page_load_timeout(TIMEOUT)
    return driver

=======
    driver.set_page_load_timeout(180)
    return driver


>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
def get_scraped_urls():
    if os.path.exists(OUTPUT_FILE):
        try:
            df = pd.read_csv(OUTPUT_FILE)
<<<<<<< HEAD
            return set(df['link'].dropna())
=======
            return set(df['url'].dropna())
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
        except pd.errors.EmptyDataError:
            print("⚠️ Output file exists but is empty. Ignoring it.")
            return set()
    return set()

<<<<<<< HEAD
=======

>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
def scrape_to_csv():
    driver = setup_driver()
    scraped_urls = get_scraped_urls()
    scraped_data = []

    try:
        driver.get(CATEGORY_URL)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

<<<<<<< HEAD
        articles = WebDriverWait(driver, 15).until(
=======
        articles = WebDriverWait(driver, 10).until(
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.north-east-grid.explained-section-grid ul li a"))
        )

        article_links = [a.get_attribute("href") for a in articles]
        for url in article_links:
            if url in scraped_urls:
                continue

            try:
                driver.get(url)
                time.sleep(3)
<<<<<<< HEAD

                headline = driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div > h1").text
                description = driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div > h2").text
                content = driver.find_element(By.CSS_SELECTOR, "#pcl-full-content").text

                try:
                    date_element = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="dateModified"]')
                    date_time = date_element.get_attribute("content")
                except:
                    date_time = datetime.now().isoformat()

                scraped_data.append({
                    "timestamp": date_time,
=======
                headline = driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div > h1").text
                content = driver.find_element(By.CSS_SELECTOR, "#pcl-full-content").text
                date_element = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="dateModified"]')
                date_time = date_element.get_attribute("content") if date_element else ""
                description = driver.find_element(By.CSS_SELECTOR, "#pcl-full-content").text


                scraped_data.append({
                    "timestamp": date_time or datetime.now().isoformat(),
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
                    "title": headline.strip(),
                    "summary": description.strip(),
                    "link": url,
                    "source": "indianexpress"
                })
                print(f"✅ Scraped: {url}")

            except Exception as e:
<<<<<<< HEAD
                logging.warning(f"⚠️ Error scraping {url}: {e}")
                print(f"⚠️ Error scraping {url}: {e}")

    except Exception as e:
        logging.error("❌ IndianExpress failed: %s", str(e))
        print(f"❌ Failed to load article list: {e}")
=======
                print(f"⚠️ Error scraping {url}: {e}")

    except Exception as e:
        print(f"❌ Failed to load article list: {e}")
        logging.error("❌ IndianExpress failed: %s", str(e))
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74

    finally:
        driver.quit()

    if scraped_data:
<<<<<<< HEAD
        df = pd.DataFrame(scraped_data).drop_duplicates(subset=["title", "link"])
=======
        df = pd.DataFrame(scraped_data).drop_duplicates(subset=["title"])
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"✅ Saved {len(df)} records to {OUTPUT_FILE}")
        logging.info("✅ IndianExpress scraped %d records", len(df))
    else:
        print("⚠️ No new IndianExpress articles found.")
