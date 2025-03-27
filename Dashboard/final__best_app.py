import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import spacy
from collections import Counter
from textblob import TextBlob

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# File path
file_name = "E:\\yahoo_news.csv"  # Update with the correct file path

# Load CSV
@st.cache_data
def load_data(file_name):
    df = pd.read_csv(file_name)
    # Check the columns to ensure we have 'date', 'time', 'short_description'
    st.write(df.columns)  # Debugging step to check column names
    df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce')
    return df

def filter_data_by_time(data, hours):
    time_limit = datetime.now() - timedelta(hours=hours)
    return data[data['timestamp'] >= time_limit]

def lda_topic_modeling(data, num_topics=5):
    # Vectorize the text data
    vectorizer = CountVectorizer(stop_words='english')
    dtm = vectorizer.fit_transform(data)
    
    # Apply LDA (Latent Dirichlet Allocation)
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(dtm)
    
    # Get topic assignments (most likely topic for each document)
    topic_assignments = lda.transform(dtm).argmax(axis=1)
    
    # Get the top words for each topic
    topics = {}
    for i, topic in enumerate(lda.components_):
        top_words_idx = topic.argsort()[-10:][::-1]
        top_words = [vectorizer.get_feature_names_out()[i] for i in top_words_idx]
        topics[f"Topic {i+1}"] = top_words
    
    return topic_assignments, topics, vectorizer

def calculate_kpi(df):
    # KPI: Count the number of news articles
    return df.shape[0]

def compute_trends(recent_data, historical_data, ngram_range=(2, 2)):
    # Compute n-grams (bigrams or trigrams) for trend analysis
    vectorizer = CountVectorizer(ngram_range=ngram_range, stop_words='english')
    recent_dtm = vectorizer.fit_transform(recent_data)
    historical_dtm = vectorizer.transform(historical_data)
    
    # Get word counts for both recent and historical data
    recent_counts = recent_dtm.sum(axis=0).A1
    historical_counts = historical_dtm.sum(axis=0).A1
    feature_names = vectorizer.get_feature_names_out()
    
    # Compute z-scores for trends
    mean_historical = np.mean(historical_counts)
    std_historical = np.std(historical_counts)
    z_scores = (recent_counts - mean_historical) / std_historical
    
    trends = pd.DataFrame({
        'ngram': feature_names,
        'count': recent_counts,
        'z_score': z_scores
    })
    
    return trends.sort_values(by='z_score', ascending=False)

def save_to_csv(df, file_name="classified_articles.csv"):
    df.to_csv(file_name, index=False)
    st.write(f"File saved: {file_name}")

# Streamlit UI
def main():
    st.title('📊 News Articles Analysis Dashboard')

    # Load the data
    df = load_data(file_name)

    st.sidebar.header("KPI Metrics")
    num_articles = calculate_kpi(df)
    st.sidebar.metric(label="Number of News Articles", value=num_articles)

    if 'short_description' in df.columns and 'timestamp' in df.columns:
        # Time Filter with longer periods
        time_filter = st.sidebar.selectbox(
            "Select Time Filter",
            ['Last 24 hours', 'Last 2 days', 'Last 4 days', 'Last 7 days', 'Last 15 days']
        )

        # Get recent data (last 24 hours)
        recent_data = filter_data_by_time(df, 24)

        # Get historical data based on the selected window (EXCLUDING recent period)
        if time_filter == 'Last 2 days':
            historical_data = df[
                (df['timestamp'] < datetime.now() - timedelta(hours=24)) & 
                (df['timestamp'] >= datetime.now() - timedelta(days=2))
            ]
        elif time_filter == 'Last 4 days':
            historical_data = df[ 
                (df['timestamp'] < datetime.now() - timedelta(hours=24)) & 
                (df['timestamp'] >= datetime.now() - timedelta(days=4))
            ]
        elif time_filter == 'Last 7 days':
            historical_data = df[ 
                (df['timestamp'] < datetime.now() - timedelta(hours=24)) & 
                (df['timestamp'] >= datetime.now() - timedelta(days=7))
            ]
        elif time_filter == 'Last 15 days':
            historical_data = df[ 
                (df['timestamp'] < datetime.now() - timedelta(hours=24)) & 
                (df['timestamp'] >= datetime.now() - timedelta(days=15))
            ]
        else:
            historical_data = recent_data

        if not recent_data.empty and not historical_data.empty:
            bigrams = compute_trends(recent_data['short_description'].dropna(), historical_data['short_description'].dropna(), ngram_range=(2, 2))
            trigrams = compute_trends(recent_data['short_description'].dropna(), historical_data['short_description'].dropna(), ngram_range=(3, 3))

            # Plot Bi-Grams
            st.subheader("🔎 Top Bi-Grams by Z-Score")
            fig, ax = plt.subplots()
            ax.bar(bigrams['ngram'][:10], bigrams['count'][:10], color='skyblue')  # Top 10 words
            ax.set_xlabel('Bi-Gram')
            ax.set_ylabel('Count')
            ax.set_title(f'Top Bi-Grams by Z-Score ({time_filter})')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)

            # Plot Tri-Grams
            st.subheader("🔎 Top Tri-Grams by Z-Score")
            fig, ax = plt.subplots()
            ax.bar(trigrams['ngram'][:10], trigrams['count'][:10], color='lightcoral')  # Top 10 words
            ax.set_xlabel('Tri-Gram')
            ax.set_ylabel('Count')
            ax.set_title(f'Top Tri-Grams by Z-Score ({time_filter})')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.warning("⚠️ No recent or historical data available.")

    # Apply LDA to the dataset and get the topics
    topic_assignments, topics, vectorizer = lda_topic_modeling(df['short_description'].dropna(), num_topics=5)
    df['category'] = topic_assignments
    
    # Topic names
    topic_names = ['Sports', 'Entertainment', 'Politics', 'Science', 'Technology']

    # Sidebar for selecting a category (e.g., Sports, Politics, Entertainment, etc.)
    st.sidebar.header("Select a News Category")
    
    # Scrollable list of categories
    selected_category = st.sidebar.selectbox("Choose a Category", topic_names)

    # Map the selected category to its corresponding topic number
    topic_map = {name: i for i, name in enumerate(topic_names)}
    
    # Get the topic number corresponding to the selected category
    selected_topic_index = topic_map[selected_category]  # Get the index (e.g., 0 for 'Sports', 1 for 'Entertainment')

    # Get the top words for the selected topic (e.g., 'Topic 1', 'Topic 2', etc.)
    selected_topic = f"Topic {selected_topic_index + 1}"  # Map the index to the corresponding topic name (e.g., 'Topic 1', 'Topic 2')

    # Fetch the top words for the selected topic from the 'topics' dictionary
    top_words = topics[selected_topic][:10]  # Get the top 10 words for the selected topic

    # Filter articles by selected category (topic)
    selected_category_data = df[df['category'] == selected_topic_index]

    # Show the articles from the selected category
    st.subheader(f"Articles from {selected_category}")
    st.write(selected_category_data[['short_description', 'category', 'timestamp']])

    # Show top 10 words for the selected topic based on LDA
    st.subheader(f"Top 10 Words in {selected_category} based on LDA")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_words, range(1, 11), color='skyblue')
    ax.set_xlabel('Words')
    ax.set_ylabel('Importance')
    ax.set_title(f'Top 10 Words in {selected_category} based on LDA')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # Save the dataset with predicted categories to a new CSV file
    save_to_csv(df)

    st.sidebar.info("Select a category to explore news articles.")

if __name__ == "__main__":
    main()
