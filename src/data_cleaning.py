import pandas as pd
from pathlib import Path

# Get project folder path
BASE_DIR = Path(__file__).resolve().parents[1]

# Load raw dataset
file_path = BASE_DIR / "data" / "raw_posts.csv"

data = pd.read_csv(file_path)

# Display original dataset
print("Original Social Media Dataset:")
print(data)

print("\nTotal Records:", len(data))
# Check duplicate posts
duplicates = data.duplicated(subset=["post_id"]).sum()

print("\nDuplicate Posts:", duplicates)
# Remove duplicate posts
data = data.drop_duplicates(subset=["post_id"])

# Display cleaned dataset
print("\nCleaned Dataset:")
print(data)

print("\nTotal Records After Cleaning:", len(data))
# Save cleaned dataset
output_path = BASE_DIR / "data" / "cleaned_posts.csv"

data.to_csv(output_path, index=False)

print("\nCleaned dataset saved successfully!")
print("Saved Location:", output_path)