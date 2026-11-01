
import pandas as pd
from pathlib import Path
from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "youtube_cleaned_posts.csv"
OUTPUT_FILE = BASE_DIR / "data" / "youtube_topic_results.csv"

print("Loading cleaned YouTube data...")

df = pd.read_csv(INPUT_FILE)
df = df.dropna(subset=["combined_text"])

documents = df["combined_text"].astype(str).tolist()

if len(documents) < 3:
    raise ValueError("At least 3 documents are required for topic detection.")

print("Total documents:", len(documents))
print("Loading BERTopic model...")

# Adjust UMAP settings for a small initial dataset
umap_model = UMAP(
    n_neighbors=min(15, len(documents) - 1),
    n_components=2,
    min_dist=0.0,
    metric="cosine",
    random_state=42
)

hdbscan_model = HDBSCAN(
    min_cluster_size=2,
    min_samples=1,
    metric="euclidean",
    cluster_selection_method="eom",
    prediction_data=True
)

topic_model = BERTopic(
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    min_topic_size=2,
    calculate_probabilities=False,
    verbose=True
)

print("\nDiscovering topics...")

topics, probabilities = topic_model.fit_transform(documents)

df["topic_id"] = topics

# Add readable topic names
topic_info = topic_model.get_topic_info()

topic_names = dict(
    zip(topic_info["Topic"], topic_info["Name"])
)

df["topic_name"] = df["topic_id"].map(topic_names)

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print("\nBERTopic analysis completed!")
print("Total documents:", len(df))
print("Topics discovered:", len(set(topics) - {-1}))
print("Saved at:", OUTPUT_FILE)

print("\nTopic summary:")
print(topic_info)

print("\nDataset preview:")
print(df[["title", "topic_id", "topic_name"]].head())
