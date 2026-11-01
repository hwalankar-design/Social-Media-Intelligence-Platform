import pandas as pd
from pathlib import Path

# Get project folder
BASE_DIR = Path(__file__).resolve().parents[1]

# Load cleaned dataset
file_path = BASE_DIR / "data" / "cleaned_posts.csv"

data = pd.read_csv(file_path)

# Display social media posts
print("Social Media Posts:")
print(data[["post_id", "post_text"]])
from textblob import TextBlob

# Create sentiment analysis function
def analyze_sentiment(text):
    analysis = TextBlob(str(text))
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"


# Apply sentiment analysis
data["sentiment"] = data["post_text"].apply(analyze_sentiment)

# Display results
print("\nSentiment Analysis Results:")
print(data[["post_text", "sentiment"]])
# Count sentiment categories
sentiment_counts = data["sentiment"].value_counts()

print("\nSentiment Summary:")
print(sentiment_counts)
# Save sentiment analysis results
output_path = BASE_DIR / "data" / "sentiment_results.csv"

data.to_csv(output_path, index=False)

print("\nSentiment results saved successfully!")
print("Saved at:", output_path)