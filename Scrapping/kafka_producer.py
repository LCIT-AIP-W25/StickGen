# kafka_producer.py
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(data, topic='news.raw'):
    producer.send(topic, value=data)
    producer.flush()
    print(f"📤 Sent to Kafka → Topic: {topic} | Title: {data['title'][:50]}...")
