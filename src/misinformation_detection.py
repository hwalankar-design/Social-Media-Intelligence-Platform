import pandas as pd
from pathlib import Path
# Get project folder path
BASE_DIR = Path(__file__).resolve().parents[1]

# Load cleaned dataset
file_path = BASE_DIR / "data" / "cleaned_posts.csv"

data = pd.read_csv(file_path)

# Display social media posts
print("Posts for Misinformation Analysis:")
print(data[["post_id", "post_text"]])
# Define suspicious keywords
suspicious_keywords = [
    "fake news",
    "100% guaranteed",
    "share immediately",
    "shocking truth",
    "secret cure",
    "forward this"
]

# Function to check suspicious posts
def detect_suspicious_post(text):
    text = str(text).lower()

    for keyword in suspicious_keywords:
        if keyword in text:
            return "Flagged for Review"

    return "No Keyword Flag Found"
# Apply suspicious post detection
data["misinformation_status"] = data["post_text"].apply(
    detect_suspicious_post
)

# Display detection results
print("\nMisinformation Detection Results:")

print(
    data[["post_id", "post_text", "misinformation_status"]]
)
# Count flagged posts
flagged_count = (
    data["misinformation_status"] == "Flagged for Review"
).sum()

safe_count = (
    data["misinformation_status"] == "No Keyword Flag Found"
).sum()

print("\nMisinformation Screening Summary:")
print("Flagged for Review:", flagged_count)
print("No Keyword Flag Found:", safe_count)
# Save misinformation detection results
output_path = BASE_DIR / "data" / "misinformation_results.csv"

data.to_csv(output_path, index=False)

print("\nMisinformation results saved successfully!")
print("Saved at:", output_path)