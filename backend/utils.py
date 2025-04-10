from diffusers import StableDiffusionPipeline
from diffusers.models.attention_processor import AttnProcessor
import torch
import time
from logger import logger
import torch._dynamo

# Suppress flash attention issues and fallback to eager mode
torch._dynamo.config.suppress_errors = True

device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if device == "cuda" else torch.float32
logger.info(f"Using device: {device} with dtype: {torch_dtype}")

# ===== Helper to disable flash attention inside UNet =====
def patch_attention(model):
    try:
        model.unet.set_attn_processor(AttnProcessor())
        logger.info("✅ Flash attention disabled via AttnProcessor.")
    except Exception as e:
        logger.warning("⚠️ Failed to patch attention processor", exc_info=True)

# --------- Load Emoji Model ---------
try:
    emoji_pipeline = StableDiffusionPipeline.from_pretrained(
        "./model",
        torch_dtype=torch_dtype,
        safety_checker=None
    ).to(device)
    patch_attention(emoji_pipeline)
    logger.info("✅ Emoji model loaded.")
except Exception as e:
    logger.error("Error loading emoji model", exc_info=True)

# --------- Load Sticker Model ---------
try:
    sticker_pipeline = StableDiffusionPipeline.from_pretrained(
        "./sticker_model",
        torch_dtype=torch_dtype,
        safety_checker=None
    ).to(device)
    patch_attention(sticker_pipeline)
    logger.info("✅ Sticker model loaded.")
except Exception as e:
    logger.error("Error loading sticker model", exc_info=True)

# --------- Emoji Generation Function ---------
def generate_emoji(text):
    try:
        logger.info(f"🟡 Generating emoji for text: {text}")
        with torch.inference_mode():
            image = emoji_pipeline(text, num_inference_steps=25).images[0]
        output_path = './static/generated.png'
        image.save(output_path)
        logger.info(f"✅ Generated emoji saved at: {output_path}")
        return output_path
    except Exception as e:
        logger.error("Error generating emoji", exc_info=True)
        raise e

# --------- Sticker Generation Function ---------
def generate_sticker(text):
    try:
        logger.info(f"🟡 Generating sticker for text: {text}")
        with torch.inference_mode():
            image = sticker_pipeline(text, num_inference_steps=25).images[0]
        output_path = './static/generated_sticker.png'
        image.save(output_path)
        logger.info(f"✅ Generated sticker saved at: {output_path}")
        return output_path
    except Exception as e:
        logger.error("Error generating sticker", exc_info=True)
        raise e
