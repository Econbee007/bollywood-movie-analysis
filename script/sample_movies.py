import os
import numpy as np
import pandas as pd 
from functools import reduce

# Set the working directory
# Change this to your actual working directory
os.chdir(r"D:\RA assessment\bollywood-movie-analysis")

# Define the file paths for the datasets
# Ensure these paths are correct relative to your working directory
file_paths = [
    os.path.join("data", "bollywood_2010-2019.csv"), #main dataset
    os.path.join("data", "bollywood_meta_2010-2019.csv"),
    os.path.join("data", "bollywood_ratings_2010-2019.csv"),
    os.path.join("data", "bollywood_text_2010-2019.csv")
]

# Load all into list of DataFrames
dfs = [pd.read_csv(fp) for fp in file_paths]

# Step 4: Merge all on 'imdb_id'
merged_df = reduce(lambda left, right: pd.merge(left, right, on='imdb_id', how='left'), dfs)

# Randomly sample 100 movies
sampled_df = merged_df.sample(n=100, random_state=42)

# Create output folder
output_dir = r"D:\RA assessment\bollywood-movie-analysis\data\sampled"
os.makedirs(output_dir, exist_ok=True)
# Save sampled data
output_path = os.path.join(output_dir, "movies_sampled.csv")
sampled_df.to_csv(output_path, index=False)











