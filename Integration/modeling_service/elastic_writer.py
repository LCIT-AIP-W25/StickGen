from elasticsearch import Elasticsearch
import os

# Replace with your Elastic Cloud URL and credentials
es = Elasticsearch(
    "https://your-cloud-cluster-url:9243",  # or use os.getenv("ES_URL")
    basic_auth=("elastic", "your-password")  # or use os.getenv("ES_USER"), os.getenv("ES_PASS")
)

def write_to_elasticsearch(article):
    index_name = "news-index"
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)

    es.index(index=index_name, document=article)
    print("📤 Indexed to ElasticSearch")
