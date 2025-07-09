import spacy
import csv
import os

nlp = spacy.load("en_core_web_sm")

input_file = "google_news_master.csv"
output_file = "google_news_with_ner.csv"

# Step 1: Load already processed titles
processed_titles = set()
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            processed_titles.add(row["Title"])

# Step 2: Open input/output files
with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "a", newline='', encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["Entities"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    # Write header only if file is new
    if os.path.getsize(output_file) == 0:
        writer.writeheader()

    new_count = 0
    for row in reader:
        if row["Title"] in processed_titles:
            continue  # Skip already processed rows

        # NER
        doc = nlp(row["Title"])
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        row["Entities"] = str(entities)
        writer.writerow(row)
        new_count += 1

print(f"✅ Processed and saved {new_count} new rows with NER to {output_file}")
