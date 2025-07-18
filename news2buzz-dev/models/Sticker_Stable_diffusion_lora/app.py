import os
import pandas as pd
from diffusers import StableDiffusionPipeline
import torch

def main():
    # Path to your CSV file
    csv_path = "preprocessed_news.csv"

    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"❌ CSV file '{csv_path}' not found. Please place it in the same folder as app.py.")
        return

    # Load the CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    # Check for required column
    if 'translated_text' not in df.columns:
        print("❌ Column 'translated_text' not found in CSV.")
        return

    # Create output directory
    output_dir = "generated_stickers"
    os.makedirs(output_dir, exist_ok=True)

    # Load Stable Diffusion model
    print("⏳ Loading Stable Diffusion model...")
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32)
    pipe.to("cpu")  # Change to "cuda" if using GPU
    print("✅ Model loaded.")

    # Loop through each prompt
    for idx, row in df.iterrows():
        prompt = str(row["translated_text"])
        if pd.isna(prompt) or prompt.strip() == "":
            print(f"⚠️ Skipping empty prompt at index {idx}")
            continue

        try:
            print(f"🎨 Generating sticker for index {idx}...")
            image = pipe(prompt).images[0]
            image_path = os.path.join(output_dir, f"sticker_{idx}.png")
            image.save(image_path)
            print(f"✅ Saved: {image_path}")
        except Exception as e:
            print(f"❌ Error generating sticker for index {idx}: {e}")

if __name__ == "__main__":
    main()
