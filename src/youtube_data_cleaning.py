
import re
import html
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "youtube_posts.csv"
OUTPUT_FILE = BASE_DIR / "data" / "youtube_cleaned_posts.csv"


def clean_text(text):
    if pd.isna(text):
        return ""

    text = html.unescape(str(text))
    text = re.sub(r"<[^>]+>", " ", text)  # Remove HTML tags
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)  # Remove URLs
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces

    return text.strip()


# Load YouTube dataset
df = pd.read_csv(INPUT_FILE)

print("Original records:", len(df))

# Remove duplicate videos
df = df.drop_duplicates(subset=["video_id"])

# Remove records without video ID or title
df = df.dropna(subset=["video_id", "title"])

# Clean title and description
df["title"] = df["title"].apply(clean_text)
df["description"] = df["description"].apply(clean_text)

# Create combined text for future NLP analysis
df["combined_text"] = (
    df["title"] + " " + df["description"]
).str.strip()

# Remove empty text records
df = df[df["combined_text"] != ""]

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print("\nYouTube data cleaning completed!")
print("Cleaned records:", len(df))
print("Dataset shape:", df.shape)
print("Saved at:", OUTPUT_FILE)

print("\nCleaned dataset preview:")
print(df[["video_id", "title", "channel_title", "views"]].head())
