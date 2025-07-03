from model_runner import run_models
from elastic_writer import write_to_elasticsearch
from mongo_writer import save_to_mongo
from sql_writer import save_to_sql

# Sample article like what you'd get from Kafka
test_article = {
    "title": "New AI Tool Outperforms GPT-4 in Coding Tasks",
    "content": "Researchers have unveiled a new AI model that surpasses GPT-4 in complex software development."
}

# Run your .pkl-based models
enriched = run_models(test_article)

# Save outputs to all storages
write_to_elasticsearch(enriched)
save_to_mongo(enriched)
save_to_sql(enriched)

print("\n✅ Test article processed and stored successfully.")
