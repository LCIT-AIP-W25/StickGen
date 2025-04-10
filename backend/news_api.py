from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def get_news_data(query):
    if query:
        response = es.search(
            index="news_articles",
            query={
                "multi_match": {
                    "query": query,
                    "fields": ["headline", "short_description", "summary", "predicted_category"]
                }
            },
            size=100
        )
    else:
        response = es.search(
            index="news_articles",
            query={"match_all": {}},
            size=100
        )

    hits = response["hits"]["hits"]
    return [hit["_source"] for hit in hits]
