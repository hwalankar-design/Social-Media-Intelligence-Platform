
import os
import json
import time
from pathlib import Path
from datetime import datetime, timezone

from dotenv import load_dotenv
from googleapiclient.discovery import build

# --------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("YOUTUBE_API_KEY")

OUTPUT_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TOPICS = [
    "Python Programming",
    "Artificial Intelligence",
    "Machine Learning",
    "Data Science",
    "Deep Learning",
    "Data Analytics",
    "Backend Development",
    "Generative AI"
]

VIDEOS_PER_TOPIC = 10

# --------------------------------
# 2. CONNECT TO YOUTUBE API
# --------------------------------

if not API_KEY:
    raise ValueError("YouTube API key not found!")

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

all_results = []

# --------------------------------
# 3. COLLECT VIDEO SEARCH RESULTS
# --------------------------------

for topic in TOPICS:

    print(f"\nCollecting topic: {topic}")

    try:
        request = youtube.search().list(
            part="snippet",
            q=topic,
            type="video",
            maxResults=VIDEOS_PER_TOPIC,
            order="relevance"
        )

        response = request.execute()

        all_results.append({
            "topic": topic,
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "response": response
        })

        print(
            "Videos collected:",
            len(response.get("items", []))
        )

        time.sleep(1)

    except Exception as error:
        print(f"Error collecting {topic}: {error}")

# --------------------------------
# 4. SAVE RAW JSON DATA
# --------------------------------

output_file = OUTPUT_DIR / "youtube_raw_data.json"

with open(output_file, "w", encoding="utf-8") as file:

    json.dump(
        all_results,
        file,
        ensure_ascii=False,
        indent=4
    )

print("\n--------------------------------")
print("YOUTUBE DATA COLLECTION FINISHED")
print("--------------------------------")

print("Topics processed:", len(TOPICS))
print("Total videos collected:", sum(
    len(item["response"].get("items", []))
    for item in all_results
))

print("Saved file:", output_file)
