#Code for Scraping URLs of News Articles from Indian Express

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to save data to CSV
def save_to_csv(data, filename):
    if data:
        unique_data = list(set(data))  # Remove duplicates
        df = pd.DataFrame(unique_data, columns=["url"])
        df.to_csv(filename, index=False, mode='a', header=not pd.io.common.file_exists(filename))
        print(f"Saved {len(unique_data)} unique URLs to {filename}")
    else:
        print("No data to save!")

# Function for manual login
def manual_login(login_url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(login_url)
    print("Please log in manually and then press Enter to continue...")
    input("Press Enter after logging in...")
    
    return driver

# Function to scrape world news URLs
def news_headlines_url_1(category_link, news_count):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(category_link)
        time.sleep(3)  # Wait for the page to load
    except Exception as e:
        print("Error loading page:", e)
        driver.quit()
        return []

    headlines_url_set = set()

    while len(headlines_url_set) < news_count:
        try:
            # Scroll to load dynamically loaded content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            # Explicitly wait for the article links to appear
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li > h2 > a"))
            )
            
            # Collect article URLs from the current page
            for element in elements:
                headline_url = element.get_attribute("href")
                if headline_url:
                    headlines_url_set.add(headline_url)
                if len(headlines_url_set) >= news_count:
                    break  # Stop if we have enough URLs

            print(f"Collected {len(headlines_url_set)} URLs so far...")

            # Find the 'Next' button and navigate to the next page
            try:
                next_button = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//a[contains(@class,"next page-numbers")]'))
                )
                next_page_url = next_button.get_attribute("href")
                if next_page_url:
                    print(f"Navigating to next page: {next_page_url}")
                    driver.get(next_page_url)
                    time.sleep(3)
                else:
                    print("No more pages or 'Next' button not found.")
                    break
            except Exception:
                print("No more pages or 'Next' button not found.")
                break

        except Exception as e:
            print("Error scraping page:", e)
            break

    driver.quit()
    save_to_csv(list(headlines_url_set), "World_headlines_urls.csv")
    return list(headlines_url_set)

# Category URL for World News
category_url = "https://indianexpress.com/section/world/"

# Login URL
login_url = "https://indianexpress.com/login"

# Step 1: Log in manually
driver = manual_login(login_url)

# Step 2: Proceed with scraping after logging in
world_headlines_url = news_headlines_url_1(category_url, 2000)

print("World news data successfully scraped and saved!")




# #Code for Scraping News Articles from Indian Express From the Collected URLs
# import time
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from tqdm import tqdm
# import os

# # Constants
# CSV_FILE = "political_headlines_urls.csv"
# OUTPUT_FILE = "political_data.csv"
# BATCH_SIZE = 200  # Number of URLs per batch
# LOGIN_URL = "https://indianexpress.com/login/"
# COOKIE_URL = "https://indianexpress.com/"  # URL to keep session active
# RETRY_LIMIT = 3  # Number of retries for each URL

# # Function to read URLs from CSV
# def read_urls_from_csv(filename):
#     df = pd.read_csv(filename)
#     return df['url'].tolist()  # Assuming CSV has a column named 'url'

# # Function to get last scraped URL
# def get_last_scraped_url(output_file):
#     if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
#         df = pd.read_csv(output_file)
#         if 'url' in df.columns and not df['url'].empty:
#             return df['url'].tolist()  # Get list of already scraped URLs
#     return []

# # Function to open login page manually and store session cookies
# def manual_login(driver):
#     print(f"Opening login page: {LOGIN_URL}")
#     driver.get(LOGIN_URL)
#     input("Log in manually, then press Enter here to continue scraping...")  # Wait for manual login
#     cookies = driver.get_cookies()  # Save login session cookies
#     return cookies  

# # Function to keep session alive by visiting the homepage
# def keep_alive(driver, cookies):
#     driver.get(COOKIE_URL)  
#     for cookie in cookies:
#         driver.add_cookie(cookie)
#     driver.refresh()
#     print("Session refreshed to prevent timeout.")

# # Function to scrape content from URLs in batches
# def scrape_urls(csv_file, output_file, batch_size):
#     all_urls = read_urls_from_csv(csv_file)
#     scraped_urls = get_last_scraped_url(output_file)

#     # Remove already scraped URLs from the list
#     url_list = [url for url in all_urls if url not in scraped_urls]
#     total_urls = len(url_list)

#     if total_urls == 0:
#         print("All URLs have already been scraped. Exiting.")
#         return

#     print(f"Resuming from {len(scraped_urls)}. {total_urls} URLs remaining.")

#     chrome_options = webdriver.ChromeOptions()
#     prefs = {"profile.managed_default_content_settings.images": 2}
#     chrome_options.add_experimental_option("prefs", prefs)
#     driver = webdriver.Chrome(options=chrome_options)

#     # Open login page and save cookies
#     cookies = manual_login(driver)

#     scraped_data = []

#     for batch_start in range(0, total_urls, batch_size):
#         batch_urls = url_list[batch_start:batch_start + batch_size]
#         print(f"Processing batch {batch_start + 1} to {batch_start + len(batch_urls)} of {total_urls}")

#         for url in tqdm(batch_urls, desc="Scraping", unit="URL"):
#             attempt = 0
#             success = False

#             while attempt < RETRY_LIMIT and not success:
#                 try:
#                     driver.get(url)
#                     time.sleep(3)

#                     headline = driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div > h1").text
#                     description = driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div > h2").text
#                     content = driver.find_element(By.CSS_SELECTOR, "#pcl-full-content").text if driver.find_elements(By.CSS_SELECTOR, "#pcl-full-content") else ""

#                     # Extract date & time
#                     date_element = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="dateModified"]')
#                     date_time = date_element.get_attribute("content") if date_element else ""

#                     scraped_data.append([headline, description, content, date_time, url])
#                     print(f"Scraped: {url}")
#                     success = True  # If successful, break retry loop

#                 except Exception as e:
#                     attempt += 1
#                     print(f"Error scraping {url}, attempt {attempt}/{RETRY_LIMIT}: {e}")
#                     time.sleep(2)  # Wait before retrying

#             if not success:
#                 print(f"Skipping {url} after {RETRY_LIMIT} failed attempts.")
#                 scraped_data.append(["", "", "", "", url])  # Log failed URL

#         # Save batch results incrementally
#         batch_df = pd.DataFrame(scraped_data, columns=['headline', 'description', 'content', 'date_time', 'url'])
#         batch_df['date_time'] = pd.to_datetime(batch_df['date_time'], errors='coerce')  # Convert to datetime
#         batch_df = batch_df.sort_values(by='date_time', ascending=False)  # Sort by latest date first
        
#         # Append new data to the CSV
#         batch_df.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
#         print(f"Batch saved. Data saved to {output_file}")

#         # Clear scraped data to avoid memory overflow
#         scraped_data.clear()

#         # Refresh session every batch
#         keep_alive(driver, cookies)

#     driver.quit()
#     print(f"Scraping complete. Data saved to {output_file}")

# # Run scraper with batching
# scrape_urls(CSV_FILE, OUTPUT_FILE, BATCH_SIZE)
