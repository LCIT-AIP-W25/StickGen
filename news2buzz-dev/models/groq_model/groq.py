import os
from flask import Flask, request, Response, request
from groq import Groq
import json
import re

app = Flask(__name__)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Emoji dictionary based on brand/news themes
EMOJI_MAP = {
    "meditation": "🧘‍♀️🧘‍♂️🕉️",
    "matcha": "🍵☘️",
    "coffee": "☕",
    "health": "💪🧬🩺",
    "climate": "🌍🌱🔥",
    "technology": "🤖💻📱",
    "fashion": "👗🛍️✨",
    "politics": "🏛️🗳️📢",
    "economy": "💰📉📈",
    "education": "📚🎓",
    "travel": "✈️🌍🧳",
    "sports": "⚽🏀🏅",
    "music": "🎵🎤🎧"
}

def get_emojis(brand, news):
    emojis = []
    combined = f"{brand} {news}".lower()
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in combined:
            emojis.extend(emoji.split())
    seen = set()
    return " ".join(e for e in emojis if not (e in seen or seen.add(e)))

# ✂️ Helper to trim to ~2 complete sentences
def trim_to_sentences(text, max_len=250):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    result = ""
    for sentence in sentences:
        if len(result) + len(sentence) + 1 <= max_len:
            result += sentence + " "
        else:
            break
    return result.strip()

@app.route("/")
def home():
    return Response(json.dumps({"message": "Groq model is running!"}, ensure_ascii=False), mimetype="application/json")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    brand = data.get("brand", "Brand")
    news = data.get("news", "")
    platform = data.get("platform", "Instagram")
    product = data.get("product", "")
    tone = data.get("tone", "quirky")

    # 🔹 Prompt designed to encourage short output
    prompt = (
        f"Write a super short {tone} social media post (1–2 sentences) "
        f"for {brand} about this news: {news}. "
        f"Platform: {platform}. Product: {product}."
    )

    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )

        raw_text = response.choices[0].message.content.strip()
        trimmed_post = trim_to_sentences(raw_text, max_len=250)

        # 🎯 Append emojis
        emoji_str = get_emojis(brand, news)
        if emoji_str:
            trimmed_post += f"  {emoji_str}"

        # ✅ Ensure emojis are returned correctly (not as \uXXXX)
        return Response(json.dumps({"post": trimmed_post}, ensure_ascii=False), mimetype="application/json")

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)