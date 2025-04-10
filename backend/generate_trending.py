from collections import defaultdict, Counter
import pymongo
import json
import os
import datetime
import numpy as np

def to_hashtag(phrase):
    return "#" + "".join(word.capitalize() for word in phrase.strip().split())

def normalize(tag):
    return tag.replace("#", "").lower()

def group_hashtags_by_substring(tags_with_mentions):
    grouped = []
    seen = set()

    tags = list(tags_with_mentions.items())

    for i in range(len(tags)):
        tag_i, count_i = tags[i]
        if tag_i in seen:
            continue

        group = [(tag_i, count_i)]
        seen.add(tag_i)

        for j in range(i + 1, len(tags)):
            tag_j, count_j = tags[j]
            if tag_j in seen:
                continue

            # If one is a prefix, suffix, or substring of another
            if tag_i in tag_j or tag_j in tag_i:
                group.append((tag_j, count_j))
                seen.add(tag_j)

        total_mentions = sum(count for _, count in group)
        representative = min((t for t, _ in group), key=len)
        grouped.append((representative, total_mentions))

    return grouped

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["news_database"]
collection = db["news_articles"]

now = datetime.datetime.utcnow()
last_24h = now - datetime.timedelta(hours=24)

time_series = defaultdict(lambda: defaultdict(int))
total_counts = Counter()

for doc in collection.find():
    timestamp_str = doc.get("timestamp", "")
    try:
        timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except:
        continue

    bigrams = doc.get("bigrams", "").split(", ") if doc.get("bigrams") else []
    trigrams = doc.get("trigrams", "").split(", ") if doc.get("trigrams") else []
    phrases = bigrams + trigrams
    hashtags = [to_hashtag(p) for p in phrases if p.strip()]

    date_key = timestamp.date()
    for tag in hashtags:
        norm_tag = normalize(tag)
        time_series[norm_tag][date_key] += 1
        total_counts[norm_tag] += 1

# Z-score
spike_scores = {}
for tag, day_counts in time_series.items():
    if len(day_counts) < 2:
        continue

    sorted_days = sorted(day_counts)
    counts = [day_counts[day] for day in sorted_days]
    mean = np.mean(counts)
    std = np.std(counts)
    if std == 0:
        continue

    today = now.date()
    today_count = day_counts.get(today, 0)
    z = (today_count - mean) / std

    if z >= 1.5:
        spike_scores[tag] = today_count * 1000

# Fallback
if not spike_scores:
    for tag, count in total_counts.items():
        spike_scores[tag] = count * 1000

# Group using substring rule
grouped = group_hashtags_by_substring(spike_scores)

# Remove similar using token overlap
sorted_all = sorted(grouped, key=lambda x: -x[1])
final_result = []
used_tokens = set()

for tag, mentions in sorted_all:
    tokens = set(tag.lower().split())
    if tokens & used_tokens:
        continue

    final_result.append({"hashtag": "#" + tag, "mentions": mentions})
    used_tokens.update(tokens)

    if len(final_result) == 5:
        break

# Save to trending.json
output_path = os.path.join("..", "frontend", "public", "trending.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_result, f, indent=2, ensure_ascii=False)

print("\u2705 trending.json saved with cleaned trending topics:", output_path)