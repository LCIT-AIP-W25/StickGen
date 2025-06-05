import spacy
import pandas as pd

nlp = spacy.load("en_core_web_sm")

def perform_ner(input_file):
    df = pd.read_csv(input_file)

    records = []
    for _, row in df.iterrows():
        doc = nlp(str(row['title']) + " " + str(row['description']))
        for ent in doc.ents:
            records.append({
                'text': ent.text,
                'label': ent.label_,
                'source': row['url']
            })

    pd.DataFrame(records).to_csv("data/ner_results.csv", index=False)
