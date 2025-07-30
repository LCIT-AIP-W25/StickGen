\# News2Buzz – NextGen Social Media Post Generator



News2Buzz is an AI-powered platform that transforms trending news into emotionally resonant, brand-aligned social media content — including posts, emojis, and stickers. This version continues the senior batch's work and focuses on building a complete AI content pipeline.



---



\## 📦 Folder Structure



news2buzz-dev/

├── backend/ # Flask APIs, Kafka consumers

├── data/ # Raw and cleaned news data

├── frontend/ # React-based UI

├── kafka\_pipeline/ # Kafka producer/consumer scripts, schemas

├── models/ # LoRA GPT-2, Stable Diffusion, and classifiers

├── notebooks/ # Research, model training, testing

├── scraper/ # News scrapers (Google, Reddit, etc.)

├── tests/ # Unit tests for each component

└── README.md # Project documentation



yaml

Copy

Edit



---



\## 👥 Team Members



\- Anjitha Mohan – Language Model Integration Specialist  

\- Jissy Jayaprakash – NLP \& Preprocessing Lead  

\- Jisna D Kunju – ML Engineer \& Personalization  

\- Suraiya Jabeen – Backend Developer  

\- Indu – Frontend Developer  

\- Natish Kumar – DB \& Testing Lead  



---



\## 🚀 Features



\- 🔍 News scraping from Reddit, NewsAPI, Google News

\- 🧠 Fake news, sentiment \& bias detection (BERT/BART models)

\- ✍️ GPT-2 LoRA fine-tuned post generation

\- 🎨 Stable Diffusion LoRA for sticker creation

\- 📡 Real-time integration with Kafka

\- 🖥️ Full-stack React + Flask architecture



---



\## ⚙️ Getting Started



```bash

\# Clone the repo

git clone https://github.com/your-org/StickGen.git



\# Navigate into the dev folder

cd StickGen/news2buzz-dev



\# Setup virtual env (optional)

python -m venv venv

venv\\Scripts\\activate



\# Install backend requirements

pip install -r backend/requirements.txt

📌 Status

This is an in-progress next-gen rebuild of the StickGen project. Kafka is partially integrated; final pipeline testing is ongoing.



📄 License

MIT License

