import psycopg2

def save_to_sql(article):
    conn = psycopg2.connect(
        host="localhost",
        database="newsdb",
        user="postgres",
        password="yourpassword"
    )
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id SERIAL PRIMARY KEY,
            title TEXT,
            content TEXT,
            sentiment TEXT,
            topic TEXT,
            bias_score REAL
        )
    ''')

    cur.execute('''
        INSERT INTO news (title, content, sentiment, topic, bias_score)
        VALUES (%s, %s, %s, %s, %s)
    ''', (
        article.get('title', ''),
        article.get('content', ''),
        article.get('sentiment', ''),
        article.get('topic', ''),
        article.get('bias_score', 0.0)
    ))

    conn.commit()
    conn.close()
    print("🧾 Saved to SQL")
