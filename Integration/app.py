from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from diffusers import StableDiffusionPipeline
import torch
import os

app = Flask(__name__)
CORS(app)

# Load fine-tuned emoji model
MODEL_PATH = "C:/Users/patel/Desktop/project_test/model"

# Try loading the model
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_PATH,
    ignore_mismatched_sizes=True,
    torch_dtype=torch.float16,
    safety_checker=None
).to("cuda")

# Create static folder if it doesn't exist
os.makedirs("static", exist_ok=True)

# Route for generating emoji
@app.route('/generate-emoji', methods=['POST'])
def generate_emoji():
    try:
        data = request.json
        prompt = data.get('prompt')

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Generate emoji using the fine-tuned model
        image = pipe(prompt).images[0]

        # Save the generated emoji
        output_path = os.path.join("static", "generated_emoji.png")
        image.save(output_path)

        return jsonify({"image_url": f"http://localhost:5000/static/generated_emoji.png"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve generated images
@app.route('/static/<filename>')
def serve_file(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
