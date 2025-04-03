from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["news_database"]
collection = db["news_articles"]

# Kafka Consumer
consumer = KafkaConsumer(
    "news_topic",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Listening for messages...")
for message in consumer:
    print(f"Saving article: {message.value['headline'][:50]}...")
    collection.insert_one(message.value)
