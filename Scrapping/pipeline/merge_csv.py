import pandas as pd
import glob
import os

def merge_all_csvs():
    temp_folder = "data/temp_sources"
    merged_file = "data/merged_news.csv"

    all_files = glob.glob(os.path.join(temp_folder, "*.csv"))
    if not all_files:
        print("⚠️ No CSV files found to merge.")
        return

    dataframes = []
    for file in all_files:
        df = pd.read_csv(file)

        # Normalize columns
        if "headline" in df.columns:
            df.rename(columns={"headline": "title"}, inplace=True)
        if "published" in df.columns:
            df.rename(columns={"published": "timestamp"}, inplace=True)
        if "source" not in df.columns:
            df["source"] = os.path.basename(file).split("_")[0]

        for col in ["timestamp", "title", "summary", "link", "source"]:
            if col not in df.columns:
                df[col] = ""

        df = df[["timestamp", "title", "summary", "link", "source"]]
        dataframes.append(df)

    combined = pd.concat(dataframes, ignore_index=True)
    combined.drop_duplicates(subset=["title"], inplace=True)
    os.makedirs("data", exist_ok=True)
    combined.to_csv(merged_file, index=False)

    print(f"✅ Merged {len(all_files)} files into {merged_file} with {len(combined)} unique rows.")
