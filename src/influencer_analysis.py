import pandas as pd
from pathlib import Path
# Get project folder path
BASE_DIR = Path(__file__).resolve().parents[1]

# Load cleaned dataset
file_path = BASE_DIR / "data" / "cleaned_posts.csv"

data = pd.read_csv(file_path)

# Display engagement data
print("Social Media Engagement Data:")

print(data[["username", "likes", "comments", "shares"]])
# Calculate engagement score
data["engagement_score"] = (
    data["likes"] +
    data["comments"] +
    data["shares"]
)

# Display engagement scores
print("\nPost Engagement Scores:")

print(data[["username", "engagement_score"]])
# Group posts by username
influencer_data = data.groupby("username")[
    "engagement_score"
].sum().reset_index()

# Rank influencers from highest to lowest
influencer_data = influencer_data.sort_values(
    by="engagement_score",
    ascending=False
)

# Display influencer ranking
print("\nTop Influencers:")
print(influencer_data)
# Save influencer analysis results
output_path = BASE_DIR / "data" / "influencer_results.csv"

influencer_data.to_csv(output_path, index=False)

print("\nInfluencer results saved successfully!")
print("Saved at:", output_path)