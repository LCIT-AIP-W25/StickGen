import time
import math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException

# Configure Selenium WebDriver for the main page (for categories)
chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.videos": 2,
    "profile.managed_default_content_settings.gifs": 2
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

# Fetch URLs of different categories from the homepage
def fetch_category_urls():
    try:
        driver.set_page_load_timeout(10)
        driver.get("https://indianexpress.com/")
    except Exception as e:
        print("Error loading website:", e)

    try:
        business_section_url = driver.find_element(By.CSS_SELECTOR, "#navbar > li:nth-child(6) > a").get_attribute("href")
        education_section_url = driver.find_element(By.CSS_SELECTOR, "#navbar > li:nth-child(13) > a").get_attribute("href")
        sports_section_url = driver.find_element(By.CSS_SELECTOR, "#navbar > li:nth-child(8) > a").get_attribute("href")
        tech_section_url = driver.find_element(By.CSS_SELECTOR, "#navbar > li:nth-child(12) > a").get_attribute("href")
        entertainment_section_url = driver.find_element(By.CSS_SELECTOR, "#navbar > li:nth-child(7) > a").get_attribute("href")
    except Exception as e:
        print("Error fetching category URLs:", e)
    
    driver.quit()

    return {
        "business": business_section_url,
        "education": education_section_url,
        "sports": sports_section_url,
        "tech": tech_section_url,
        "entertainment": entertainment_section_url
    }

# Save data to CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=["url"])  # Create a DataFrame with a single 'url' column
    df.to_csv(filename, index=False, mode='a', header=not pd.io.common.file_exists(filename))  # Append to CSV if it exists

# Function to scrape news headlines from a category
def news_headlines_url_1(category_link, news_count):
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.videos": 2,
        "profile.managed_default_content_settings.gifs": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.set_page_load_timeout(15)
        driver.get(category_link)
    except Exception as e:
        print(e)
        pass
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    elements_per_page = 25
    total_pages = math.ceil(news_count / elements_per_page)
    headlines_url_list = []

    for page in tqdm(range(total_pages), desc="Processing", unit="iteration"):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, "div.img-context>h2>a")  # Find the required web element
            for element in elements:
                if len(headlines_url_list) >= news_count:  # Breaks the loop if the list reaches needed quantity
                    break
                headline_url = element.get_attribute("href")  # Getting hyperlink from the web element
                headlines_url_list.append(headline_url)

            next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@class="next page-numbers"]')))
            next_button.click()

        except Exception as e:
            print(e)
            pass

    return headlines_url_list

# Function to extract content from article pages
def content_extraction(url_list, category):
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.videos": 2,
        "profile.managed_default_content_settings.gifs": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    
    # Lists for storing extracted data
    headlines_list = []
    description_list = []
    content_list = []

    for url in tqdm(url_list, desc="Extracting Content", unit="URL"):
        try:
            driver.set_page_load_timeout(10)
            driver.get(url)
            time.sleep(3)

            # Extract the content, title, and description
            headline = driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div > h1").text
            description = driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div > h2").text
            content = driver.find_element(By.CSS_SELECTOR, "#pcl-full-content").text if driver.find_elements(By.CSS_SELECTOR, "#pcl-full-content") else ""

            headlines_list.append(headline)
            description_list.append(description)
            content_list.append(content)

            print(f"Extracted data from: {url}")

        except Exception as e:
            print(f"Error extracting data from {url}: {e}")
            headlines_list.append("")
            description_list.append("")
            content_list.append("")

    # Save extracted data to CSV row by row
    for i in range(len(headlines_list)):
        save_to_csv([{
            'headline': headlines_list[i],
            'description': description_list[i],
            'content': content_list[i],
            'url': url_list[i],
            'category': category
        }], "scraped_news_data.csv")

    driver.quit()

# Main process to fetch category URLs and scrape headlines/content
def main():
    # Fetch category URLs from the homepage
    category_urls = fetch_category_urls()

    for category, url in category_urls.items():
        print(f"Scraping {category} category...")
        
        # Scrape headlines URLs for the current category (e.g., business, education)
        headlines_urls = news_headlines_url_1(url, 2000)  # 2000 can be adjusted as per the required count

        # Save headlines URLs to CSV
        save_to_csv(headlines_urls, f"{category}_headlines_urls.csv")

        # Extract content for each article URL in the category
        content_extraction(headlines_urls, category)

    print("Full process completed successfully!")

if __name__ == "__main__":
    main()
