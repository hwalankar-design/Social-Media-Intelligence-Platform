
import os
from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Find the main project folder
BASE_DIR = Path(__file__).resolve().parents[1]

# Load API key from .env
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    print("ERROR: YouTube API key not found!")
else:
    try:
        # Connect to YouTube API
        youtube = build(
            "youtube",
            "v3",
            developerKey=API_KEY
        )

        # Test the API connection
        request = youtube.search().list(
            part="snippet",
            q="Python programming",
            type="video",
            maxResults=5
        )

        response = request.execute()

        print("SUCCESS! YouTube API connected.")
        print("\nVideos found:")

        for video in response.get("items", []):
            title = video["snippet"]["title"]
            channel = video["snippet"]["channelTitle"]

            print("\nTitle:", title)
            print("Channel:", channel)

    except Exception as error:
        print("YouTube API connection failed!")
        print("Error:", error)
