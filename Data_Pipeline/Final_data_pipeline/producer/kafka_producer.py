from kafka import KafkaProducer
import json
import time

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Sample articles to send to Kafka
articles = [
    {"headline": "Breaking News: AI Revolutionizes Tech Industry", "content": "AI is transforming the way we work and live."},
    {"headline": "Sports Update: Local Team Wins Championship", "content": "The local team secured a historic victory."},
    {"headline": "Weather Alert: Heavy Rain Expected Tomorrow", "content": "Prepare for heavy rain and possible flooding."}
]

print("Sending messages to Kafka...")
for article in articles:
    print(f"Sending article: {article['headline'][:50]}...")
    producer.send("news_topic", article)
    time.sleep(1)  # Simulate delay between messages