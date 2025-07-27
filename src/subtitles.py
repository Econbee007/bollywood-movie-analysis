# %%
import os
import time
import re
import requests
import pandas as pd
from dotenv import load_dotenv

# === Load environment variables from .env file ===
load_dotenv()
API_KEY = os.getenv("OPENSUBTITLES_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please set OPENSUBTITLES_API_KEY in your .env file.")

HEADERS = {
    "Api-Key": API_KEY,
    "User-Agent": "BollywoodSubDownloader v1.0"
}

# === Set working directories ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
SAMPLE_PATH = os.path.join(PROJECT_DIR, "data", "sampled", "movies_sampled.csv")
SUBTITLE_DIR = os.path.join(PROJECT_DIR, "data", "subtitles")
os.makedirs(SUBTITLE_DIR, exist_ok=True)

# === Load sampled movies ===
df = pd.read_csv(SAMPLE_PATH)

# === List to collect subtitle text ===
subtitle_data = []

# === Function to download subtitle and return file path ===
def download_subtitle(imdb_id, title):
    print(f"\n🔍 Searching subtitle for: {title} ({imdb_id})")

    search_url = "https://api.opensubtitles.com/api/v1/subtitles"
    params = {
        "languages": "en",
        "order_by": "download_count",
        "order_direction": "desc",
        "type": "movie"
    }

    if pd.notna(imdb_id) and isinstance(imdb_id, str) and imdb_id.startswith("tt"):
        params["imdb_id"] = imdb_id
    else:
        params["query"] = title

    try:
        response = requests.get(search_url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"❌ Search failed. Status code: {response.status_code}")
            return None
        data = response.json()
    except Exception as e:
        print(f"❌ Exception during search: {e}")
        return None

    if not data.get("data"):
        print("⚠️ No subtitles found.")
        return None

    try:
        file_id = data["data"][0]["attributes"]["files"][0]["file_id"]
    except Exception as e:
        print(f"⚠️ Subtitle found, but no downloadable file: {e}")
        return None

    try:
        download_url = "https://api.opensubtitles.com/api/v1/download"
        download_response = requests.post(download_url, headers=HEADERS, json={"file_id": file_id})
        if download_response.status_code != 200:
            print(f"❌ Failed to get download link. Status code: {download_response.status_code}")
            return None
        link_data = download_response.json()
        link = link_data.get("link")
    except Exception as e:
        print(f"❌ Exception while getting download link: {e}")
        return None

    if not link:
        print("⚠️ No download link returned.")
        return None

    safe_name = imdb_id if pd.notna(imdb_id) else title
    safe_name = re.sub(r'[<>:"/\\|?*]', '-', str(safe_name))
    file_path = os.path.join(SUBTITLE_DIR, f"{safe_name}.srt")

    try:
        srt = requests.get(link).content
        with open(file_path, "wb") as f:
            f.write(srt)
        print(f"✅ Subtitle saved: {file_path}")
        return file_path
    except Exception as e:
        print(f"❌ Failed to save subtitle: {e}")
        return None

# === Loop through each row in dataset ===
print("\n🚀 Starting subtitle download process...")

for _, row in df.iterrows():
    imdb_id = row.get("imdb_id", None)
    title = row.get("original_title", "Unknown Title")

    if pd.isna(title) or not isinstance(title, str):
        continue

    subtitle_path = download_subtitle(imdb_id, title)
    if subtitle_path and os.path.exists(subtitle_path):
        try:
            with open(subtitle_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            subtitle_data.append({
                "imdb_id": imdb_id,
                "original_title": title,
                "subtitle_text": text
            })
        except Exception as e:
            print(f"⚠️ Could not read {subtitle_path}: {e}")

    time.sleep(2)  # Respect rate limits

# === Save to CSV with append logic ===
combined_csv_path = os.path.join(SUBTITLE_DIR, "subtitles_all.csv")

if os.path.exists(combined_csv_path):
    existing_df = pd.read_csv(combined_csv_path)
    updated_df = pd.concat([existing_df, pd.DataFrame(subtitle_data)], ignore_index=True)
else:
    updated_df = pd.DataFrame(subtitle_data)

# Drop duplicates based on imdb_id
updated_df = updated_df.drop_duplicates(subset="imdb_id", keep="last")

# Save to CSV
updated_df.to_csv(combined_csv_path, index=False, encoding="utf-8")
print(f"\n📁 All subtitles saved to: {combined_csv_path}")

