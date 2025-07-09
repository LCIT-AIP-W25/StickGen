import pandas as pd
import glob
import os
<<<<<<< HEAD

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
=======
from datetime import datetime
import shutil

def merge_all_csvs():
    temp_folder = "data/temp_sources"
    master_file = "data/merged_news.csv"

    # Step 1: Backup existing merged_news.csv
    if os.path.exists(master_file):
        today = datetime.now().strftime("%Y-%m-%d")
        backup_file = f"data/merged_news_backup_{today}.csv"
        shutil.copy(master_file, backup_file)
        print(f"🛡️ Backup created: {backup_file}")
        df_master = pd.read_csv(master_file)
    else:
        df_master = pd.DataFrame(columns=["timestamp", "title", "summary", "link", "source"])

    # Step 2: Load new scraped CSVs
    all_files = glob.glob(os.path.join(temp_folder, "*.csv"))
    new_dataframes = []

    for file in all_files:
        try:
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
            new_dataframes.append(df)

        except Exception as e:
            print(f"⚠️ Skipped {file} due to error: {e}")

    if not new_dataframes:
        print("⚠️ No new valid CSVs to merge.")
        return

    df_new = pd.concat(new_dataframes, ignore_index=True)

    # Step 3: Combine with existing master file
    combined = pd.concat([df_master, df_new], ignore_index=True)
    combined.drop_duplicates(subset=["title"], keep="last", inplace=True)

    # Step 4: Save final merged file
    os.makedirs("data", exist_ok=True)
    combined.to_csv(master_file, index=False)

    print(f"✅ Successfully merged {len(all_files)} new files into merged_news.csv.")
    print(f"📦 Final row count: {len(combined)}")

# Run this when needed (or from Flask)
if __name__ == "__main__":
    merge_new_data_into_master()
>>>>>>> 6e2e9f0c6c7363898fec9ebeee28917ae81e8b74
