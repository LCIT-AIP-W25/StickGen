import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_to_json():
    url = "https://www.bbc.com/news"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for link in soup.find_all("a", href=True):
        href = link['href']
        text = link.get_text(strip=True)
        if "/news/" in href and text and len(text.split()) > 4:
            full_url = f"https://www.bbc.com{href}"
            try:
                article_resp = requests.get(full_url, headers=headers, timeout=5)
                article_soup = BeautifulSoup(article_resp.text, "html.parser")
                paragraphs = article_soup.find_all("p")
                summary_text = " ".join(p.get_text() for p in paragraphs[:3])
            except:
                summary_text = text
            articles.append({
                "timestamp": datetime.now().isoformat(),
                "title": text,
                "summary": summary_text or text,
                "link": full_url,
                "source": "bbc"
            })

    return articles
