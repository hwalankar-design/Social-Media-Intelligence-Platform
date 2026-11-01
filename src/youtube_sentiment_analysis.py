
import pandas as pd
from pathlib import Path
from transformers import pipeline

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "youtube_cleaned_posts.csv"
OUTPUT_FILE = BASE_DIR / "data" / "youtube_sentiment_results.csv"

MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

print("Loading YouTube dataset...")

df = pd.read_csv(INPUT_FILE)

if df.empty:
    raise ValueError("The YouTube dataset is empty.")

print("Total videos:", len(df))
print("\nLoading multilingual Transformer model...")
print("The first download may take several minutes.")

sentiment_model = pipeline(
    "sentiment-analysis",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME
)

print("\nAnalyzing sentiment...")

texts = df["combined_text"].fillna("").astype(str).tolist()

predictions = sentiment_model(
    texts,
    batch_size=8,
    truncation=True,
    max_length=512
)

df["sentiment"] = [
    prediction["label"] for prediction in predictions
]

df["sentiment_score"] = [
    round(prediction["score"], 4) for prediction in predictions
]

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print("\nMultilingual sentiment analysis completed!")
print("Total analyzed videos:", len(df))
print("Saved at:", OUTPUT_FILE)

print("\nSentiment distribution:")
print(df["sentiment"].value_counts())

print("\nDataset preview:")
print(df[["title", "sentiment", "sentiment_score"]].head())
