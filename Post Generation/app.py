from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Initialize Flask app
app = Flask(__name__)

# Load base model + tokenizer + LoRA fine-tuned weights
base_model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = PeftModel.from_pretrained(base_model, "./lora-output")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)

# ✅ Tone-specific prompt loader (limit to 6–8 matching tone examples)
def load_few_shot_prompt_by_tone(tone="quirky", max_examples=8):
    with open("few_shot_prompt.txt", "r", encoding="utf-8") as f:
        blocks = f.read().strip().split("Example ")
    filtered = [f"Example {b}" for b in blocks if f"Tone: {tone}" in b]
    return "\n".join(filtered[:max_examples])

@app.route('/generate_post', methods=['POST'])
def generate_post():
    data = request.get_json()

    news = data.get("news", "")
    brand = data.get("brand", "")
    product = data.get("product", "")
    tone = data.get("tone", "quirky")
    platform = data.get("platform", "Instagram")

    # ✅ Use filtered prompt examples based on requested tone
    few_shot = load_few_shot_prompt_by_tone(tone)

    # Build prompt
    prompt = f"""{few_shot}

Now your turn:
News: {news}
Brand: {brand}"""
    if product:
        prompt += f"\nProduct: {product}"
    prompt += f"\nTone: {tone}\nPost (1 sentence showing {tone} tone, for {platform}, include emojis and hashtags):"

    # Generate output
    try:
        output = generator(prompt, max_new_tokens=60, do_sample=True, top_k=50, top_p=0.95, temperature=0.9)
        generated_text = output[0]["generated_text"]
        final_post = generated_text.split("Post:")[-1].split("\n")[0].strip()
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
