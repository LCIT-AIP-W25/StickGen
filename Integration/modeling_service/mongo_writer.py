from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["news_db"]
collection = db["news_articles"]

def save_to_mongo(article):
    collection.insert_one(article)
    print("🍃 Saved to MongoDB")
