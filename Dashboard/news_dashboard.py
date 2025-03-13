import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from bertopic import BERTopic
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel
from contractions import fix
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import nltk

# Download nltk resources
nltk.download('punkt')
nltk.download('stopwords')

# Load stopwords
stop_words = set(stopwords.words('english'))
custom_stopwords = {"said", "say", "new", "one", "year", "also", "would", "u", "could", "may"}
stop_words.update(custom_stopwords)

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Load dataset
@st.cache_data
def load_data():
    file_path = "C:/Users/patel/Desktop/final year/news_database.news_articles.csv"
    df = pd.read_csv(file_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    df["date"] = df["timestamp"].dt.date
    return df

# Preprocessing function
def preprocess_text(text):
    text = str(text).lower()
    text = fix(text)  # Expand contractions
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # Remove URLs
    text = re.sub(r"\d+", "", text)  # Remove numbers
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
    text = re.sub(r"\s+", " ", text).strip()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

# Sentiment analysis function
def get_sentiment(text):
    if isinstance(text, str):
        score = analyzer.polarity_scores(text)
        if score['compound'] >= 0.05:
            return 'Positive'
        elif score['compound'] <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    return 'Neutral'

# Load data
df = load_data()

# Preprocess text
df['processed_text'] = (df['headline'].fillna('') + ' ' + df['short_description'].fillna('')).apply(preprocess_text)

# Generate sentiment
df['sentiment'] = df['processed_text'].apply(get_sentiment)

# -------- LDA MODEL --------
def train_lda():
    dictionary = Dictionary([text.split() for text in df['processed_text']])
    corpus = [dictionary.doc2bow(text.split()) for text in df['processed_text']]
    
    lda_model = LdaModel(corpus=corpus, num_topics=5, id2word=dictionary, passes=10)
    
    df['lda_topic'] = [max(lda_model.get_document_topics(corpus[i]), key=lambda x: x[1])[0] for i in range(len(corpus))]
    topic_keywords = {i: ", ".join([word for word, _ in lda_model.show_topic(i, 5)]) for i in range(5)}
    df['lda_topic_words'] = df['lda_topic'].map(topic_keywords)

train_lda()

# -------- BERTopic --------
@st.cache_data
def train_bertopic():
    topic_model = BERTopic(n_gram_range=(1, 3), min_topic_size=5)
    topics, _ = topic_model.fit_transform(df['processed_text'])
    df['bertopic'] = topics
    topic_info = topic_model.get_topic_info()
    topic_labels = {row['Topic']: row['Name'] for _, row in topic_info.iterrows()}
    df['bertopic_words'] = df['bertopic'].map(topic_labels).fillna('Uncategorized')

train_bertopic()

# ==================================
# -------- STREAMLIT UI -----------
# ==================================
st.title("📊 Real-Time Trend Detection Dashboard")

# -------- SUMMARY SECTION --------
st.subheader("📌 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("📰 Total Articles", len(df))
col2.metric("🔥 Unique Topics", len(df['lda_topic'].unique()))
col3.metric("🚀 Most Popular Topic", df['lda_topic_words'].value_counts().index[0])

# -------- TRENDING TOPICS --------
st.subheader("🔥 Top Trending Topics")
top_topics = df['lda_topic_words'].value_counts().head(10)
fig = px.bar(top_topics, x=top_topics.index, y=top_topics.values, text=top_topics.values)
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
st.plotly_chart(fig)

# -------- TREND OVER TIME --------
st.subheader("📈 Trend Over Time")
trend_data = df.groupby(['date', 'lda_topic_words']).size().reset_index(name='count')
fig = px.line(trend_data, x='date', y='count', color='lda_topic_words', markers=True)
st.plotly_chart(fig)

# -------- SENTIMENT ANALYSIS --------
st.subheader("😀 Sentiment Analysis")
sentiment_data = df['sentiment'].value_counts()
fig = px.pie(sentiment_data, values=sentiment_data.values, names=sentiment_data.index)
st.plotly_chart(fig)

# -------- GEOGRAPHIC INSIGHTS --------
st.subheader("🌍 Geographic Insights")
if 'country' in df.columns:
    geo_data = df.groupby('country').size().reset_index(name='count')
    fig = px.choropleth(geo_data, locations='country', locationmode='country names', color='count', color_continuous_scale='Viridis')
    st.plotly_chart(fig)

# -------- NETWORK GRAPH --------
st.subheader("🔗 Topic Relationship Graph")
G = nx.Graph()
for topic in df['lda_topic_words'].unique():
    G.add_node(topic)
    for related_topic in df['lda_topic_words'].sample(3):
        G.add_edge(topic, related_topic)

pos = nx.spring_layout(G)
fig, ax = plt.subplots(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_size=12, font_color='black', font_weight='bold', edge_color='gray')
st.pyplot(fig)

# -------- SEARCH AND FILTER --------
st.subheader("🔍 Search and Filter")
search_term = st.text_input("Search Topic:")
filtered_data = df[df['lda_topic_words'].str.contains(search_term, case=False)] if search_term else df
st.dataframe(filtered_data[['headline', 'short_description', 'lda_topic_words', 'sentiment']])

# -------- EXPORT RESULTS --------
if st.button("Export Results to CSV"):
    filtered_data.to_csv("filtered_trends.csv", index=False)
    st.success("✅ Exported to filtered_trends.csv")

# -------- NOTIFICATIONS --------
if df['lda_topic_words'].value_counts().max() > 100:
    st.warning(f"⚠️ High Volume Detected for '{df['lda_topic_words'].value_counts().index[0]}'!")

# ==================================
# -------- RUN DASHBOARD ----------
# ==================================
# To run:
# streamlit run trend_dashboard.py
