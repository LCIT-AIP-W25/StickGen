from kafka import KafkaConsumer, KafkaProducer
import json
from model_runner import run_models
from elastic_writer import write_to_elasticsearch
from mongo_writer import save_to_mongo
from sql_writer import save_to_sql

def start_kafka_worker():
    consumer = KafkaConsumer(
        'news.cleaned',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='latest',
        group_id='modeling-group'
    )

    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    print("🟢 Kafka consumer started...")
    for msg in consumer:
        article = msg.value
        print(f"\n📥 Received article: {article.get('title', '')[:60]}")

        try:
            enriched = run_models(article)
            producer.send("news.labeled", value=enriched)
            print("✅ Produced to news.labeled")

            write_to_elasticsearch(enriched)
            save_to_mongo(enriched)
            save_to_sql(enriched)

        except Exception as e:
            print(f"❌ Error processing message: {e}")
