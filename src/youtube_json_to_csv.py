
import json
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data"

INPUT_FILE = RAW_DIR / "youtube_video_statistics.json"
OUTPUT_FILE = OUTPUT_DIR / "youtube_posts.csv"

# Load JSON data
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    videos = json.load(file)

rows = []

# Extract useful fields
for video in videos:

    snippet = video.get("snippet", {})
    statistics = video.get("statistics", {})
    content = video.get("contentDetails", {})

    rows.append({
        "video_id": video.get("id"),
        "title": snippet.get("title"),
        "description": snippet.get("description"),
        "channel_id": snippet.get("channelId"),
        "channel_title": snippet.get("channelTitle"),
        "published_at": snippet.get("publishedAt"),
        "views": int(statistics.get("viewCount", 0)),
        "likes": int(statistics.get("likeCount", 0)),
        "comments": int(statistics.get("commentCount", 0)),
        "duration": content.get("duration")
    })

# Create DataFrame
df = pd.DataFrame(rows)

# Save CSV
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print("YouTube JSON converted to CSV successfully!")
print("Total videos:", len(df))
print("Dataset shape:", df.shape)
print("Saved at:", OUTPUT_FILE)

print("\nDataset preview:")
print(df.head())
