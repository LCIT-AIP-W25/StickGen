from flask import Flask, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")

# Add a home route
@app.route('/')
def home():
    return "Welcome to the News2Buzz API! Visit /news to see data."

@app.route('/news', methods=['GET'])
def get_news():
    res = es.search(index="news-index", query={"match_all": {}}, size=100)
    data = [doc["_source"] for doc in res["hits"]["hits"]]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
