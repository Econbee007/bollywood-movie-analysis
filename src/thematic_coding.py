import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from tqdm import tqdm

# === Step 1: Setup ===
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("API key not found. Please set GEMINI_API_KEY in your .env file.")

genai.configure(api_key=GOOGLE_API_KEY)
# Use a stable and supported model
model = genai.GenerativeModel("models/gemini-2.5-pro")

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

# === Step 4: Define prompts ===
themes = [
    "Hindu–Muslim relations",
    "Gender relations",
    "Nationalism"
]

custom_theme = "Attitude towards caste hierarchy"

def make_prompt(text):
    return f"""
Analyze the following movie content (subtitle + description) and code it for the following themes:

1. Hindu–Muslim relations: Exclusionary, Inclusive, Neutral
2. Gender relations: Progressive, Conservative, Neutral
3. Nationalism: Positive, Negative, Neutral
4. Attitude towards caste hierarchy: Reinforcing, Challenging, Neutral

Respond in JSON with keys: hindu_muslim, gender, nationalism, caste

TEXT:
{text}
"""

# === Step 5: Run classification ===
thematic_results = []

for _, row in tqdm(df.iterrows(), total=len(df)):
    imdb_id = row.get("imdb_id")
    title = row.get("original_title")
    text = row.get("combined_text")

    if not text or len(text.strip()) < 100:
        print(f"⏩ Skipping {title} due to short text.")
        continue

    try:
        prompt = make_prompt(text[:12000])  # Gemini token limits
        response = model.generate_content(prompt)
        result = response.text.strip()
        
        # Try parsing JSON-like response
        result_dict = eval(result) if result.startswith("{") else {"raw": result}

        result_dict.update({"imdb_id": imdb_id, "original_title": title})
        thematic_results.append(result_dict)

    except Exception as e:
        print(f"⚠️ Error for {title}: {e}")
        thematic_results.append({"imdb_id": imdb_id, "original_title": title, "error": str(e)})

# === Step 6: Save output ===
os.makedirs(DATA_DIR, exist_ok=True)
output_df = pd.DataFrame(thematic_results)
output_path = os.path.join(DATA_DIR, "thematic_coding.csv")
output_df.to_csv(output_path, index=False, encoding="utf-8")
print(f"\n🎉 Thematic coding saved to {output_path}") 
