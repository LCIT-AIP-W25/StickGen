from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import re

app = Flask(__name__)

# Load model + tokenizer
base_model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = PeftModel.from_pretrained(base_model, "./lora-output")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)

# ✅ Load few-shot examples with graceful fallback
def load_few_shot_prompt_by_tone(tone="quirky", max_examples=6):
    try:
        with open("few_shot_prompt.txt", "r", encoding="utf-8") as f:
            blocks = f.read().strip().split("\n\n")
        filtered = [b for b in blocks if f"Tone: {tone}" in b]
        if not filtered:
            print(f"[Warning] No examples found for tone='{tone}'. Falling back to 'quirky'.")
            filtered = [b for b in blocks if "Tone: quirky" in b]
        return "\n\n".join(filtered[:max_examples]) if filtered else ""
    except FileNotFoundError:
        return "[Error] few_shot_prompt.txt not found."

# ✅ Clean + check brand inclusion and quality
def validate_post(post_text, brand):
    if not post_text or len(post_text.strip().split()) < 4:
        return False
    if re.search(r"http[s]?://", post_text):  # avoid links
        return False
    if brand.lower() not in post_text.lower():
        return False
    return True

@app.route('/generate_post', methods=['POST'])
def generate_post():
    data = request.get_json()
    news = data.get("news", "")
    brand = data.get("brand", "")
    product = data.get("product", "")
    platform = data.get("platform", "Instagram")
    tone = data.get("tone", "quirky").strip().lower()

    # Load few-shot
    few_shot = load_few_shot_prompt_by_tone(tone)

    # Build smart prompt
    prompt = f"""{few_shot}

Now your turn:
Write a {tone} social media post for the brand "{brand}".
News: {news}"""
    if product:
        prompt += f"\nProduct: {product}"

    prompt += f"""
Platform: {platform}
Instructions:
- Write 1 short, brand-aware sentence in {tone} tone.
- Do NOT reply with only hashtags or links.
- Include the brand "{brand}" naturally in the sentence.
- Use emojis and 1–2 relevant hashtags.
- Keep it original, platform-suitable, and engaging.

Post:"""

    try:
        output = generator(
            prompt,
            max_new_tokens=100,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.95
        )
        raw_output = output[0]["generated_text"]
        final_post = raw_output.split("Post:")[-1].strip().split("\n")[0]
        final_post = re.split(r'(?<=[.!?])\s', final_post)[0].strip()

        # ✅ Validation
        if not validate_post(final_post, brand):
            fallbacks = {
                "quirky": f"{brand} just launched a new product... or a pizza into orbit. 🍕🚀 #WhatJustHappened",
                "poetic": f"{brand} moves like moonlight on tides of change. 🌙🌊 #EleganceInAction",
                "empathetic": f"{brand} stands with those affected. You're not alone. 💚 #TogetherWeCare",
                "sarcastic": f"{brand} solving global crises one hashtag at a time. 🙄 #VeryHelpful",
                "serious": f"{brand} recognizes the importance of this issue and calls for action. 🧠 #ThinkActChange",
                "corporate": f"{brand} remains committed to innovation and integrity. 📊 #LeadershipInAction",
                "activist": f"{brand} stands for impact. Let’s make change matter. 🌍✨ #ActNow #BrandWithPurpose"
            }
            final_post = fallbacks.get(tone, f"{brand} makes headlines, with a bold voice. #OnTheMove")

    except Exception as e:
        final_post = f"⚠️ Error generating post: {str(e)}"

    return jsonify({
        "news": news,
        "brand": brand,
        "tone": tone,
        "platform": platform,
        "product": product,
        "post": final_post
    })

if __name__ == '__main__':
    app.run(debug=True, port=8001)
