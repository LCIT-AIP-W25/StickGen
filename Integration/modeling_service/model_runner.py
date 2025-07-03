from bertopic import BERTopic
import pickle

# Correct way to load BERTopic model
topic_model = BERTopic.load("bertopic_model_cpu.pkl")

# Sentiment model (still use pickle)
with open("sentiment_model_cpu.pkl", "rb") as f:
    sentiment_model = pickle.load(f)

def run_models(article):
    content = article.get("content", "")
    
    sentiment = sentiment_model(content)[0]['label']
    topics, _ = topic_model.transform([content])
    topic = topic_model.get_topic_name(topics[0])

    article['sentiment'] = sentiment
    article['topic'] = topic
    article['bias_score'] = 0.1

    return article
