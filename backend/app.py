from flask import Flask, request, jsonify, send_from_directory
import json
import torch
import os
from logger import logger
from flask_cors import CORS
from utils import generate_emoji, generate_sticker
from elasticsearch import Elasticsearch

# ==== App Config ====
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ==== Ensure static folder exists ====
if not os.path.exists('static'):
    os.makedirs('static')
import redis
redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

# ==== Connect to Elasticsearch ====
es = Elasticsearch("http://localhost:9200")

# ========== Emoji Route ==========
@app.route('/generate_emoji', methods=['POST'])
def generate_emoji_route():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        if not text:
            return jsonify({'error': 'Text is missing'}), 400

        logger.info(f"Generating emoji for: {text}")
        output_path = generate_emoji(text)
        return jsonify({'url': f'http://127.0.0.1:5001/static/generated.png'})
    
    except Exception as e:
        logger.error("Error generating emoji", exc_info=True)
        return jsonify({'error': str(e), 'details': repr(e)}), 500
        #return jsonify({'error': str(e)}), 500

# ========== Sticker Route ==========
@app.route('/generate_sticker', methods=['POST'])
def generate_sticker_route():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        if not text:
            return jsonify({'error': 'Text is missing'}), 400

        logger.info(f"Generating sticker for: {text}")
        output_path = generate_sticker(text)
        return jsonify({'url': f'http://127.0.0.1:5001/static/generated_sticker.png'})
    
    except Exception as e:
        logger.error("Error generating sticker", exc_info=True)
        return jsonify({'error': str(e), 'details': repr(e)}), 500
        #return jsonify({'error': str(e)}), 500

# ========== News API Route ==========
@app.route('/api/news', methods=['GET'])
def get_news_route():
    query = request.args.get('query', '').strip().lower()
    cache_key = f"news:{query or 'all'}"

    try:
        # ✅ Check Redis cache first
        cached_data = redis_client.get(cache_key)
        if cached_data:
            logger.info(f"Serving cached results for query: {query}")
            return jsonify(json.loads(cached_data))

        # 🔍 If not cached, fetch from Elasticsearch
        if query:
            logger.info(f"Searching news with query: {query}")
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
            logger.info("Fetching all news articles")
            response = es.search(
                index="news_articles",
                query={"match_all": {}},
                size=100
            )

        hits = response['hits']['hits']
        news_data = [hit['_source'] for hit in hits]

        # ✅ Cache the result for 1 hour (3600 seconds)
        redis_client.setex(cache_key, 3600, json.dumps(news_data))

        return jsonify(news_data)

    except Exception as e:
        logger.error("Error fetching news from Elasticsearch", exc_info=True)
        return jsonify({'error': 'Failed to fetch news'}), 500


# ========== Static Files Route ==========
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# ========== Main ==========
if __name__ == '__main__':
    logger.info("Starting Flask app on port 5001")
    app.run(debug=True, port=5001)
