import os
import pandas as pd
from diffusers import StableDiffusionPipeline
import torch
from datetime import datetime, timezone, timedelta
from dateutil import parser

def parse_mixed_dates(date_str):
    try:
        return parser.parse(date_str)
    except Exception:
        return pd.NaT

def main():
    csv_path = "News_Articles.csv"

    if not os.path.exists(csv_path):
        print(f"❌ CSV file '{csv_path}' not found. Please place it in the same folder as app.py.")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    required_columns = ['translated_text', 'datetime', 'custom_topic', 'sentiment']
    for col in required_columns:
        if col not in df.columns:
            print(f"❌ Required column '{col}' not found in CSV.")
            return

    print("Parsing mixed-format datetime values...")
    df['datetime'] = df['datetime'].apply(parse_mixed_dates)
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce', utc=True)

    df = df.dropna(subset=['datetime'])
    if df.empty:
        print("❌ No valid datetime values after conversion.")
        return

    # Define date range: one week before May 26, 2025
    end_date = datetime(2025, 6, 26, tzinfo=timezone.utc)
    start_date = end_date - timedelta(days=7)
    print(f"Filtering news from {start_date.date()} to {end_date.date()}")

    df_filtered = df[(df['datetime'] >= start_date) & (df['datetime'] < end_date)]

    if df_filtered.empty:
        print(f"⚠ No news items found in the range {start_date.date()} to {end_date.date()}")
        return

    # Keep only one row per (custom_topic, sentiment) group
    df_unique = df_filtered.dropna(subset=['custom_topic', 'sentiment', 'translated_text'])
    df_unique = df_unique.drop_duplicates(subset=['custom_topic', 'sentiment'])

    print(f"✅ Found {len(df_unique)} unique (topic, sentiment) pairs to generate stickers.")

    output_dir = "generated_stickers"
    os.makedirs(output_dir, exist_ok=True)

    print(f"⏳ Loading Stable Diffusion model (CPU optimized)...")
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float32
    )
    pipe = pipe.to("cpu")
    pipe.enable_attention_slicing()

    for _, row in df_unique.iterrows():
        prompt = str(row['translated_text'])
        topic = str(row['custom_topic']).strip().lower().replace(" ", "_")
        sentiment = str(row['sentiment']).strip().lower()

        if not prompt or pd.isna(prompt):
            print(f"⚠ Skipping empty prompt for ({topic}, {sentiment})")
            continue

        try:
            print(f"🎨 Generating sticker for Topic: {topic}, Sentiment: {sentiment}...")
            image = pipe(prompt, height=256, width=256).images[0]
            image_path = os.path.join(output_dir, f"sticker_{topic}_{sentiment}.png")
            image.save(image_path)
            print(f"✅ Saved: {image_path}")
        except Exception as e:
            print(f"❌ Error generating sticker for ({topic}, {sentiment}): {e}")

if __name__ == "__main__":
    main()