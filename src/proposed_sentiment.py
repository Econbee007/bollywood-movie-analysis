import os
import pandas as pd

# === Step 2: Load subtitle and description data ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

sub_path = os.path.join(DATA_DIR, "subtitles", "subtitles_all.csv")
desc_path = os.path.join(DATA_DIR, "descriptions", "descriptions_all.csv")

subtitle_df = pd.read_csv(sub_path)
description_df = pd.read_csv(desc_path)

# === Step 3: Merge subtitle and description ===
df = pd.merge(subtitle_df, description_df, on="imdb_id", how="outer")
df["combined_text"] = df["subtitle_text"].fillna("") + "\n" + df["plot"].fillna("")
movies_path = os.path.join(DATA_DIR, "sampled", "movies_sampled.csv")
movies_df = pd.read_csv(movies_path)[["imdb_id", "original_title"]]
df = df.merge(movies_df, on="imdb_id", how="left")

def detect_violence(text):
    keywords = [
        "kill", "murder", "violence", "gun", "fight", "blood", "terrorist", "attack", "riot",
        "war", "shoot", "bomb", "stab", "explosion", "rebel", "hostage", "brutal", "torture"
    ]
    if not isinstance(text, str) or len(text.strip()) == 0:
        return "Unclear"

    count = sum(word in text.lower() for word in keywords)
    if count >= 5:
        return "High"
    elif 1 <= count < 5:
        return "Low"
    else:
        return "Unclear"

df["violence_representation"] = df["combined_text"].apply(detect_violence)

# === Save the output ===
output_df = df[["imdb_id", "original_title", "violence_representation"]].copy()
output_path = os.path.join(DATA_DIR, "violence_measure.csv")
output_df.to_csv(output_path, index=False, encoding="utf-8")

print(f"✅ Violence coding saved to: {output_path}")