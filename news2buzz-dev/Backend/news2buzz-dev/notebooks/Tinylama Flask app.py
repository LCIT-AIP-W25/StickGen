from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import re

app = Flask(__name__)

# Load TinyLlama model (CPU-efficient)
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
text_gen = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Tone descriptions (tone → tone_style)
tone_styles = {
    "quirky": "funny, playful, and unexpected",
    "sarcastic": "witty and ironic",
    "serious": "professional and informative",
    "activist": "urgent and emotional",
    "corporate": "formal and brand-safe"
}

# Format prompt by injecting brand, tone, tone_style, news
def format_prompt(template, news, brand, tone):
    tone_style = tone_styles.get(tone, tone)  # fallback if tone not in list
    try:
        return template.format(news=news, brand=brand, tone=tone, tone_style=tone_style)
    except KeyError as e:
        raise ValueError(f"Missing placeholder in template: {e}")

# Generate post from prompt
def generate_text(prompt, max_tokens=100):
    result = text_gen(prompt, max_new_tokens=max_tokens, temperature=0.9)
    return result[0]['generated_text'].strip()

def refine_text(initial_post, brand, tone):
    review_prompt = f"Rewrite this post in a '{tone}' tone for the brand '{brand}':\n\n{initial_post}"
    result = text_gen(review_prompt, max_new_tokens=150, temperature=0.9)
    generated = result[0]['generated_text']

    # Remove everything before the first quote or colon
    cleaned = re.split(r'["“”\':]\s*', generated, maxsplit=1)[-1]

    # Keep only first 1-2 sentences (usually enough for a caption)
    sentences = re.split(r'(?<=[.!?])\s+', cleaned.strip())
    final_output = ' '.join(sentences[:2]).strip()

    # Remove weird characters
    final_output = final_output.encode("ascii", "ignore").decode()

    return final_output


@app.route('/generate_post', methods=['POST'])
def generate_post():
    data = request.json
    text = data.get("text")
    tone = data.get("tone")
    brand = data.get("brand")
    template = data.get("template")
    refine = data.get("refine", False)

    if not all([text, tone, brand, template]):
        return jsonify({"error": "Missing one or more required fields."}), 400

    try:
        prompt = format_prompt(template, text, brand, tone)
        initial_post = generate_text(prompt)

        if refine:
            final_post = refine_text(initial_post, brand, tone)
            return jsonify({
                "generated_post": final_post
            })

        return jsonify({
            "generated_post": initial_post,
            "refined": False,
            "prompt_used": prompt
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

