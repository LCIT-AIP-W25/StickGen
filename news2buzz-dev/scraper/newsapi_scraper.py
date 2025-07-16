from newsapi import NewsApiClient
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def scrape_to_json():
    newsapi = NewsApiClient(api_key='3c5d328a803b44c78e084511cb340611')  # Replace with your actual key
    queries = ["technology", "world", "business"]
    articles = []

    for q in queries:
        response = newsapi.get_everything(q=q, language='en', page_size=10)
        for a in response.get('articles', []):
            try:
                article_resp = requests.get(a['url'], timeout=5)
                soup = BeautifulSoup(article_resp.text, "html.parser")
                paragraphs = soup.find_all("p")
                summary = " ".join(p.get_text() for p in paragraphs[:5]).strip()
            except:
                summary = a.get('description') or 'No summary'

            articles.append({
                'timestamp': a.get('publishedAt', datetime.now().isoformat()),
                'title': a.get('title', 'No title'),
                'summary': summary,
                'link': a.get('url'),
                'source': 'newsapi',
                'topic': str(q)
            })

    return articles
