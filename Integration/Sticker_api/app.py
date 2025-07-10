from flask import Flask, request, send_file, jsonify, render_template
import torch
from diffusers import StableDiffusionPipeline
from peft import LoraConfig, get_peft_model, set_peft_model_state_dict
import uuid

app = Flask(__name__)

# ✅ Load model on CPU
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32
).to("cpu")

pipe.unet.eval()
pipe.text_encoder.eval()

# ✅ Load LoRA weights
unet_config = LoraConfig(
    r=8, lora_alpha=32,
    target_modules=["attn1.to_q", "attn1.to_k", "attn1.to_v", "attn2.to_out.0"],
    lora_dropout=0.1, bias="none"
)
clip_config = LoraConfig(
    r=8, lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "out_proj"],
    lora_dropout=0.1, bias="none"
)

pipe.unet = get_peft_model(pipe.unet, unet_config).to("cpu")
pipe.text_encoder = get_peft_model(pipe.text_encoder, clip_config).to("cpu")

set_peft_model_state_dict(pipe.unet, torch.load("unet_lora.pth", map_location="cpu"))
set_peft_model_state_dict(pipe.text_encoder, torch.load("text_encoder_lora.pth", map_location="cpu"))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        if not prompt:
            return render_template("index.html", error="Please enter a prompt.")

        image = pipe(prompt).images[0]
        filename = f"static/{uuid.uuid4().hex}.png"
        image.save(filename)

        return render_template("index.html", prompt=prompt, image_file=filename)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

