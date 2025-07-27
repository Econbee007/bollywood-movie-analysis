# %%
import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise ValueError("API key not found. Please set TMDB_API_KEY in your .env file.")

# === Setup directories ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
SAMPLE_PATH = os.path.join(PROJECT_DIR, "data", "sampled", "movies_sampled.csv")
POSTER_DIR = os.path.join(PROJECT_DIR, "data", "posters")
os.makedirs(POSTER_DIR, exist_ok=True)

# === Load sampled movies ===
df = pd.read_csv(SAMPLE_PATH)

# === Helper: Search TMDB movie and get poster URL ===
def get_poster_url(imdb_id):
    tmdb_url = f"https://api.themoviedb.org/3/find/{imdb_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "external_source": "imdb_id"
    }

    response = requests.get(tmdb_url, params=params)
    if response.status_code != 200:
        print(f"❌ TMDB request failed for {imdb_id}. Status: {response.status_code}")
        return None

    data = response.json()
    movie_results = data.get("movie_results", [])
    if not movie_results:
        print(f"❌ No TMDB movie match for {imdb_id}")
        return None

    poster_path = movie_results[0].get("poster_path")
    if not poster_path:
        print(f"⚠️ No poster path for {imdb_id}")
        return None

    return f"https://image.tmdb.org/t/p/w500{poster_path}"

# === Download posters ===
poster_records = []

print("Starting poster download...")
for _, row in df.iterrows():
    imdb_id = row.get("imdb_id")
    title = row.get("original_title", "Unknown")

    if pd.isna(imdb_id):
        continue

    poster_url = get_poster_url(imdb_id)
    if not poster_url:
        continue

    # Download image
    try:
        img_data = requests.get(poster_url).content
        filename = f"{imdb_id}.jpg"
        save_path = os.path.join(POSTER_DIR, filename)

        with open(save_path, "wb") as f:
            f.write(img_data)

        print(f"✅ Poster saved: {save_path}")

        poster_records.append({
            "imdb_id": imdb_id,
            "original_title": title,
            "poster_path": os.path.relpath(save_path, PROJECT_DIR)
        })
    except Exception as e:
        print(f"❌ Failed to download poster for {imdb_id}: {e}")

    time.sleep(1.5)  # Respect TMDB rate limits

# === Save metadata to CSV ===
poster_df = pd.DataFrame(poster_records)
poster_df.to_csv(os.path.join(PROJECT_DIR, "data", "posters", "posters_all.csv"), index=False)
print("🎉 All posters metadata saved to posters_all.csv")