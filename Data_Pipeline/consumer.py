from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Kafka Consumer Configuration
consumer = KafkaConsumer(
    'news',  # Kafka topic name
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # Start reading from the beginning of the topic
    enable_auto_commit=True,  # Automatically commit the message offset
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize JSON messages
)

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")  # Connect to MongoDB
db = client['news_db']  # Use or create a database
collection = db['articles']  # Use or create a collection

# Consume Messages from Kafka and Store in MongoDB
for message in consumer:
    article = message.value  # Get the article from the Kafka message

    # Check if the article already exists in MongoDB to avoid duplicates
    if not collection.find_one({'url': article.get('url')}):
        # Insert the article into MongoDB
        collection.insert_one({
            'title': article.get('title', ''),
            'description': article.get('description', ''),
            'content': article.get('content', ''),  # Short content from NewsAPI
            'full_content': article.get('full_content', ''),  # Full scraped content
            'url': article.get('url', ''),
            'publishedAt': article.get('publishedAt', ''),
            'source': article.get('source', {}).get('name', '')  # Source name
        })
        print(f"Inserted into MongoDB: {article.get('title')}")
    else:
        print(f"Duplicate skipped: {article.get('title')}")

# Close the MongoDB connection
client.close()
