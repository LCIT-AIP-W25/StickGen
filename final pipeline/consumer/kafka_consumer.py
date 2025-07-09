from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["news_database"]
collection = db["news_articles"]

# Kafka Consumer setup
consumer = KafkaConsumer(
    "news_topic",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("✅ Listening for messages from Kafka...")

for message in consumer:
    data = message.value

    # Construct the full document with all expected fields
    document = {
        "headline": data.get("headline"),
        #"headline_clean": data.get("headline_clean"),
        #"headline_entities": data.get("headline_entities"),
        "short_description": data.get("short_description"),
        #"short_description_clean": data.get("short_description_clean"),
        #"short_description_entities": data.get("short_description_entities"),
        "link": data.get("link"),
        "timestamp": data.get("timestamp"),
        "predicted_category": data.get("predicted_category"),
        "sentiment": data.get("sentiment"),
        #"sentiment_scores": data.get("sentiment_scores"),
        "named_entities": data.get("named_entities"),
        "summary": data.get("summary"),
        "bigrams": data.get("bigrams"),
        "trigrams": data.get("trigrams")
    }

    print(f"📝 Saving article to MongoDB: {document['headline'][:60]}")
    collection.insert_one(document)
