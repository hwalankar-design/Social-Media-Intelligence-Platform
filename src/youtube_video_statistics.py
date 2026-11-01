
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Project directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Load API key
load_dotenv(BASE_DIR / ".env")
API_KEY = os.getenv("YOUTUBE_API_KEY")

# File paths
RAW_DIR = BASE_DIR / "data" / "raw"

INPUT_FILE = RAW_DIR / "youtube_raw_data.json"
OUTPUT_FILE = RAW_DIR / "youtube_video_statistics.json"

if not API_KEY:
    raise ValueError("YouTube API key not found!")

# Load collected search results
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    collected_data = json.load(file)

# Extract unique video IDs
video_ids = set()

for topic_data in collected_data:
    for video in topic_data["response"].get("items", []):
        video_id = video["id"].get("videoId")

        if video_id:
            video_ids.add(video_id)

video_ids = sorted(video_ids)

print("Unique video IDs found:", len(video_ids))

# Connect to YouTube
youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

# Collect statistics in batches of 50
all_statistics = []

for start in range(0, len(video_ids), 50):

    batch = video_ids[start:start + 50]

    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(batch)
    )

    response = request.execute()

    all_statistics.extend(response.get("items", []))

# Save original statistics response items
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(
        all_statistics,
        file,
        ensure_ascii=False,
        indent=4
    )

print("\nVideo statistics collected successfully!")
print("Videos with statistics:", len(all_statistics))
print("Saved at:", OUTPUT_FILE)
