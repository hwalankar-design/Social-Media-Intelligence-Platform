import pandas as pd
import re
from pathlib import Path
from collections import Counter
# Get project folder path
BASE_DIR = Path(__file__).resolve().parents[1]

# Load cleaned dataset
file_path = BASE_DIR / "data" / "cleaned_posts.csv"

data = pd.read_csv(file_path)

# Display post text
print("Social Media Posts:")
print(data["post_text"])
# Text cleaning function
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text


# Apply text cleaning
data["cleaned_text"] = data["post_text"].apply(clean_text)

# Display cleaned posts
print("\nCleaned Social Media Posts:")
print(data["cleaned_text"])
# Combine all cleaned posts
all_text = " ".join(data["cleaned_text"])

# Split text into individual words
words = all_text.split()

# Count word frequency
word_counts = Counter(words)

# Display 10 most common words
print("\nMost Frequently Used Words:")

for word, count in word_counts.most_common(10):
    print(word, ":", count)
    # Common English stopwords
stopwords = {
    "is", "the", "a", "an", "in", "and",
    "to", "of", "for", "on", "are", "this",
    "it", "with", "was", "i", "my"
}

# Remove stopwords
filtered_words = [
    word for word in words
    if word not in stopwords
]

# Count meaningful words
topic_counts = Counter(filtered_words)

print("\nTop Meaningful Topics:")

for word, count in topic_counts.most_common(10):
    print(word, ":", count)
    # Save topic detection results
topic_df = pd.DataFrame(
    topic_counts.most_common(10),
    columns=["topic", "frequency"]
)

output_path = BASE_DIR / "data" / "topic_results.csv"

topic_df.to_csv(output_path, index=False)

print("\nTopic results saved successfully!")
print("Saved at:", output_path)