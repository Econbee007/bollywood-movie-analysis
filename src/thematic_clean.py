import pandas as pd
import ast
import os

# === Define paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
SAMPLED_DIR = os.path.join(DATA_DIR, "sampled")

# Paths to files
input_path = os.path.join(DATA_DIR, "thematic_coding.csv")
movies_path = os.path.join(SAMPLED_DIR, "movies_sampled.csv")
output_path = os.path.join(DATA_DIR, "thematic_coding_clean.csv")

# === Load data ===
df = pd.read_csv(input_path)
movies_df = pd.read_csv(movies_path)[["imdb_id", "original_title", "year_of_release"]].drop_duplicates()

# === Function to clean and parse raw JSON text ===
def parse_raw(raw_text):
    try:
        if isinstance(raw_text, str):
            cleaned = raw_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[len("```json"):].strip()
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3].strip()
            return ast.literal_eval(cleaned)
    except Exception:
        return {}
    return {}

# === Parse and expand JSON ===
parsed_df = df["raw"].apply(parse_raw).apply(pd.Series)

# === Join parsed data with imdb_id ===
df_clean = pd.concat([df[["imdb_id"]], parsed_df], axis=1)

# === Merge with movie titles and actual year ===
df_clean = df_clean.merge(movies_df, on="imdb_id", how="left")

# === Rename and reorder columns ===
df_clean = df_clean.rename(columns={"year_of_release": "year"})
df_clean = df_clean[["imdb_id", "original_title", "year", "hindu_muslim", "gender", "nationalism", "caste"]]

# === Reshape to long format ===
long_df = df_clean.melt(
    id_vars=["imdb_id", "original_title", "year"],
    value_vars=["hindu_muslim", "gender", "nationalism", "caste"],
    var_name="theme",
    value_name="sentiment_category"
)

# === Drop incomplete rows ===
long_df = long_df.dropna(subset=["sentiment_category"])

# === Save final cleaned file ===
long_df.to_csv(output_path, index=False, encoding="utf-8")
print(f"✅ Cleaned + merged file saved to {output_path}")
