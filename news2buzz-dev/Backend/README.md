# 🧠 News2Buzz Backend API (.NET Core)

The News2Buzz Backend API is a robust and scalable `.NET Core Web API` that powers the AI-driven News2Buzz platform. This backend facilitates seamless communication between the frontend dashboard, AI model services, and the SQL Server database. It delivers secure authentication, intelligent news filtering, and extensible endpoints for AI-generated content.

## ✅ Key Responsibilities

### 🔍 News Intelligence APIs

Provide enriched news filtering and full-text search based on:

- **Sentiment**: Positive, Negative, Neutral
- 
- **Bias**: Left-wing, Right-wing, Neutral
- 
- **Topic Modeling**: Detected via NLP/BERTopic models
- 
- **Truth Prediction**: Fake vs Real news (using LIAR dataset models)

### 🔐 Secure Authentication & Authorization

Implements full JWT-based user authentication:
- `POST /api/Auth/register` — Register users  
- `POST /api/Auth/login` — Authenticate and return token  
- `POST /api/Auth/forgot-password` — Send password reset link  
- `POST /api/Auth/reset-password` — Reset user password securely  

### 🤖 AI Model Integration Hooks

This backend provides endpoints and service scaffolds for:
- **GPT-2 / LLaMA Text Generation** — Social post creation aligned to brand tone  
- **Emoji Recommendation** — DeepMoji model or LLM-driven emoji sentiment  
- **Sticker Generation** — Supports Stable Diffusion or custom image pipelines  

### 📆 Post Scheduling (Pluggable Infrastructure)

Designed to support:
- Future integration with post schedulers (e.g., Hootsuite, Buffer)
- Queued post publishing via Kafka or Celery workers
- Admin moderation workflows

## 🧰 Tech Stack

| Layer         | Technology                |
|---------------|----------------------------|
| Backend API   | .NET 10 (Preview)          |
| ORM           | Entity Framework Core      |
| Database      | SQL Server (SSMS)          |
| Authentication| JWT Tokens                 |
| Docs          | Swagger / OpenAPI          |
| AI Integration| REST hooks, Kafka-ready    |


## 🗂 Folder Structure


Backend/

├── Controllers/ # API route handlers

├── DTOs/ # Request/Response models

├── Models/ # DB and ML classes

├── Services/ # Business logic

├── Data/ # EF Core DB context & migrations

├── final_news.csv # Enriched news dataset

├── appsettings.json # Environment configuration

└── README.md # You are here                                                                                                                                                                                                                          

## 🏃 Getting Started

# Restore NuGet packages

dotnet restore

# Package Installations

dotnet add package Microsoft.AspNetCore.Identity.EntityFrameworkCore

dotnet add package Microsoft.EntityFrameworkCore.SqlServer

dotnet add package Microsoft.EntityFrameworkCore.Tools

dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer

# Apply database migrations

dotnet ef database update

# Run the application


dotnet watch run                                                                                                                   
wagger UI available at:

➡️ http://localhost:5269/swagger                                                                                                                                                                                                                         📊 CSV Data Overview

The final_news.csv file contains pre-processed news articles enriched with:

Sentiment labels (positive, negative, neutral)

Bias classification (left/right/neutral)

Topic clusters

Fake vs real prediction

You can load this into the SQL Server database or use it for demo endpoints.         


  
  👩‍💻 Maintainers

Suraiya Jabeen – Backend Developer

Natish Kumar – Database & Testing


## 🧩 Database Schema Overview

The system uses a SQL Server database with Entity Framework Core migrations.

**Main Tables:**

- `Users` – Stores user credentials and roles  
- `NewsArticles` – Holds enriched news with sentiment, bias, topic, truth score  
- `ScheduledPosts` – (Planned) Stores user posts and schedule time  
- `Feedback` – (Planned) Captures user ratings for AI-generated posts

### Entity Relationship (ER) Snapshot:

[Users] 1 --- * [ScheduledPosts]
[Users] 1 --- * [Feedback]
[NewsArticles] 1 --- * [Feedback]

## 📫 Postman Collection

📬 Postman Collection

To test API endpoints, import this collection into [Postman](https://www.postman.com/):

📁 [`Backend/docs/News2Buzz_Backend.postman_collection.json`](./docs/News2Buzz_Backend.postman_collection.json)

It includes:
- User authentication flows
- News filtering
- CRUD for scheduled posts (planned)


