import os
import numpy as np
import pandas as pd 
from functools import reduce

# Set the working directory based on script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

# Define correct output directory for sampled data
output_dir = os.path.join(PROJECT_DIR, "data", "sampled")
os.makedirs(output_dir, exist_ok=True)  # Make sure it exists

# Define paths for merging
file_paths = [
    os.path.join(PROJECT_DIR, "data", "bollywood_2010-2019.csv"),
    os.path.join(PROJECT_DIR, "data", "bollywood_meta_2010-2019.csv"),
    os.path.join(PROJECT_DIR, "data", "bollywood_ratings_2010-2019.csv"),
    os.path.join(PROJECT_DIR, "data", "bollywood_text_2010-2019.csv")
]

# Load all CSVs
dfs = [pd.read_csv(fp) for fp in file_paths]

# Merge on 'imdb_id'
merged_df = reduce(lambda left, right: pd.merge(left, right, on='imdb_id', how='left'), dfs)

# Sample 100 random movies
sampled_df = merged_df.sample(n=100, random_state=42)

# Save sampled data
output_path = os.path.join(output_dir, "movies_sampled.csv")
sampled_df.to_csv(output_path, index=False)

print(f"✅ Sample saved to: {output_path}")
