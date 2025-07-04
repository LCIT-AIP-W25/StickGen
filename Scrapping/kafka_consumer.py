# kafka_consumer.py
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'news.raw',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='news-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("📥 Consumer started. Waiting for messages on 'news.raw'...")

for msg in consumer:
    article = msg.value
    print(f"\n📰 Title: {article['title']}")
    print(f"🧾 Summary: {article['summary'][:100]}...")
    print(f"🔗 Link: {article['link']}")
    # TODO: Call preprocessing here or push to news.cleaned topic
