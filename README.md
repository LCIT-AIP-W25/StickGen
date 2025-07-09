# StickGen

# Real-Time News Analysis and Social Media Engagement System

## Overview
This project builds a **real-time pipeline** for scraping, analyzing news articles, detecting trends/topics, and generating **stickers and emojis** to enhance social media engagement. Users can search, analyze, and share trending content via an **intuitive UI**.

## Features

### 📡 Real-Time News Scraping and Ingestion  
- Scrapes news from [NewsAPI](https://newsapi.org/) and [GDELT](https://www.gdeltproject.org/).
- Uses **Kafka** for real-time ingestion.
- Stores raw articles in **MongoDB**.

### 🔍 Data Preprocessing and Analysis  
- NLP-based **text cleaning and tokenization**.
- **Elasticsearch** for indexing and querying.
- **Redis** for caching trending articles.

### 📊 Trend & Topic Detection  
- Uses **LDA/BERTtopic** for topic modeling.
- Displays **trending topics** via Kibana dashboards.

### 🎨 Sticker & Emoji Generation  
- Uses **Diffusion models & GANs** to create stickers.
- Generates **emojis** from text sentiment & topics.
- **Dataset sources**: [Anonymous0722](https://anonymous0722.github.io/), [OpenMoji](https://openmoji.org/), [Twemoji](https://uvaauas.figshare.com/articles/dataset/Twemoji_Dataset/5822100).

### 🕵️‍♂️ Smart Search Functionality  
- **Faceted search, full-text search, synonym detection** (via Elasticsearch).
- **Sentiment & trend filters** for refined results.

### 🖥️ User Interface (UI)  
- **React.js or Flask** for a responsive UI.
- **Visualization tools** for trends and analytics.
- **Social media sharing** for stickers/emojis.

---

Let me know if you need further improvements! 🚀

