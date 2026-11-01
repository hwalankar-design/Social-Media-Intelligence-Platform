import pandas as pd

# Load social media dataset
data = pd.read_csv("data/raw_posts.csv")

# Display all posts
print(data)

# Display total number of posts
print("\nTotal Posts:", len(data))
# Display dataset information
print("\nDataset Shape:", data.shape)

# Display column names
print("\nColumn Names:")
print(data.columns.tolist())
# Check missing values
print("\nMissing Values:")
print(data.isnull().sum())