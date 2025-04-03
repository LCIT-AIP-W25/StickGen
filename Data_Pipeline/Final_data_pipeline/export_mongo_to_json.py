from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["news_database"]
collection = db["news_articles"]

# Fetch all documents from MongoDB
data = collection.find({}, {"_id": 0})  # Exclude MongoDB's `_id` field

# Save to JSON file in Logstash-compatible format (one JSON per line)
with open("news_articles.json", "w") as f:
    for document in data:
        json.dump(document, f)
        f.write("\n")  # Ensure newline after each JSON object

print("MongoDB data exported successfully! Saved as news_articles.json")
