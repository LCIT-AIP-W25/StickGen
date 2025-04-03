import nltk
import spacy
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from transformers import pipeline as hf_pipeline
import hashlib
import json
import logging
import time
import random
import re
import html
from datetime import datetime
import csv

# ---- Setup ----
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")
nltk.download("vader_lexicon")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
sia = SentimentIntensityAnalyzer()
nlp = spacy.load("en_core_web_sm")

# Zero-shot classifier (from Hugging Face)
classifier = hf_pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

candidate_labels = [
    "Politics", "Business", "Technology", "Health", "Sports",
    "Entertainment", "Science", "Crime", "Education"
]

# LDA Setup
vectorizer = TfidfVectorizer(stop_words='english')
lda = LatentDirichletAllocation(n_components=10, random_state=42)

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Selenium imports
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from kafka import KafkaProducer
from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline

# ---- Setup for T5 summarizer ----
tokenizer = T5Tokenizer.from_pretrained("t5-base")
t5_model = T5ForConditionalGeneration.from_pretrained("t5-base")
summarizer = pipeline("summarization", model=t5_model, tokenizer=tokenizer)

# Kafka Setup
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "news_topic"
BASE_URL = 'https://ca.news.yahoo.com/'

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def clean_text(text):
    text = html.unescape(text.lower())
    text = re.sub(r'http\S+|www\.\S+|\S+@\S+|@\w+|#\w+', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_wordnet_pos(tag):
    return {'J': wordnet.ADJ, 'V': wordnet.VERB, 'N': wordnet.NOUN, 'R': wordnet.ADV}.get(tag[0], wordnet.NOUN)

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    tagged = pos_tag(tokens)
    return " ".join([lemmatizer.lemmatize(word, get_wordnet_pos(pos)) for word, pos in tagged])

def get_sentiment(text):
    if not isinstance(text, str) or not text.strip():
        return "Neutral"
    score = sia.polarity_scores(text)['compound']
    return "Positive" if score > 0.05 else "Negative" if score < -0.05 else "Neutral"

def extract_entities(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ in {"PERSON", "ORG", "GPE", "EVENT", "PRODUCT"}]

def extract_summary(text):
    if not isinstance(text, str) or len(text.split()) < 50:
        return text
    summary = summarizer(text, max_length=60, min_length=5, do_sample=False)
    return summary[0]['summary_text']

def extract_ngrams(text, n=2):
    try:
        vec = CountVectorizer(ngram_range=(n, n), stop_words='english')
        X = vec.fit_transform([text])
        return ", ".join(vec.get_feature_names_out())
    except:
        return ""

def classify_news(text):
    if not text.strip():
        return "Uncategorized", 0.0
    result = classifier(text, candidate_labels)
    label = result['labels'][0]
    score = result['scores'][0]
    return (label if score > 0.05 else "Uncertain"), score

def scrape_and_process(processed_hashes):
    driver = setup_driver()
    driver.get(BASE_URL)
    time.sleep(3)

    articles = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(3):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        news_items = soup.find_all('li', class_='js-stream-content')
        for item in news_items:
            try:
                headline = item.find('h3').get_text(strip=True) if item.find('h3') else 'No Title'
                link = item.find('a')['href'] if item.find('a') else ''
                description = item.find('p').get_text(strip=True) if item.find('p') else 'No Description'
                full_link = f'https://ca.news.yahoo.com{link}' if link.startswith('/') else link

                uid = hashlib.sha256((headline + full_link).encode()).hexdigest()
                if uid in processed_hashes:
                    continue

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cleaned_h = clean_text(headline)
                cleaned_d = clean_text(description)
                pre_h = preprocess_text(cleaned_h)
                pre_d = preprocess_text(cleaned_d)
                full_text = pre_h + " " + pre_d

                sentiment = get_sentiment(full_text)
                entities = extract_entities(headline + " " + description)
                summary = extract_summary(headline + ". " + description)
                bigrams = extract_ngrams(full_text, 2)
                trigrams = extract_ngrams(full_text, 3)

                predicted_category, confidence = classify_news(headline + " " + description)

                article = {
                    "headline": headline,
                    "link": full_link,
                    "short_description": description,
                    "timestamp": timestamp,
                    "cleaned_text": full_text,
                    "sentiment": sentiment,
                    "named_entities": entities,
                    "summary": summary,
                    "bigrams": bigrams,
                    "trigrams": trigrams,
                    "predicted_category": predicted_category,
                    "confidence_score": confidence,
                }

                articles.append(article)
                processed_hashes.add(uid)
                logging.info(f"Scraped: {headline[:60]}...")

            except Exception as e:
                logging.error(f"Error: {e}")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 4))
        if driver.execute_script("return document.body.scrollHeight") == last_height:
            break
        last_height = driver.execute_script("return document.body.scrollHeight")

    driver.quit()

    # Save to CSV
    if articles:
        csv_file = "C:/Users/Acer/Desktop/news_output.csv"
        keys = articles[0].keys()
        with open(csv_file, "w", newline="", encoding="utf-8") as output:
            writer = csv.DictWriter(output, fieldnames=keys)
            writer.writeheader()
            writer.writerows(articles)
        logging.info(f"Saved {len(articles)} articles to {csv_file}")

    return articles

def send_to_kafka(data):
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    for d in data:
        producer.send(KAFKA_TOPIC, d)
        logging.info(f"Sent to Kafka: {d['headline'][:100]}")
    producer.flush()
    producer.close()

if __name__ == "__main__":
    seen = set()
    start_time = time.time()
    while time.time() - start_time < 300:  # 5 minutes
        logging.info("Starting new scrape + NLP + Zero-shot classification cycle...")
        articles = scrape_and_process(seen)
        if articles:
            send_to_kafka(articles)
        else:
            logging.info("No new articles.")
        time.sleep(300)  # 5 minutes
