import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# === Step 1: Set working directory ===
os.chdir(r"D:\RA assessment\bollywood-movie-analysis\venv")

# === Step 2: Load environment variables ===
load_dotenv()
OMDB_API_KEY = os.getenv("OPENDESCRIPTION_API_KEY")

if not OMDB_API_KEY:
    raise ValueError("API key not found. Please set OPENDESCRIPTION_API_KEY in your .env file.")

# === Step 3: Load sampled movie data ===
df = pd.read_csv("data/sampled/movies_sampled.csv")

# === Step 4: Create output directory for .txt files ===
output_dir = "data/descriptions"
os.makedirs(output_dir, exist_ok=True)

# === Step 5: Prepare list for CSV ===
plot_data = []

# === Step 6: Download and save descriptions ===
for _, row in df.iterrows():
    imdb_id = row.get("imdb_id")
    title = row.get("original_title")

    if not imdb_id:
        continue

    params = {
        "apikey": OMDB_API_KEY,
        "i": imdb_id,
        "plot": "full",
        "r": "json"
    }

    response = requests.get("http://www.omdbapi.com/", params=params)

    try:
        data = response.json()
    except Exception as e:
        print(f"❌ JSON decode error for {title}: {e}")
        continue

    if data.get("Response") == "True":
        plot = data.get("Plot", "No plot available.")
        filename = f"{imdb_id}.txt"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(plot)

        # ✅ Add to combined CSV data
        plot_data.append({
            "imdb_id": imdb_id,
            "original_title": title,
            "plot": plot
        })

        print(f"✅ Saved description for: {title}")
    else:
        print(f"❌ Plot not found for: {title} ({imdb_id})")

    time.sleep(1.5)  # Respect OMDb rate limit

# === Step 7: Save all collected descriptions into one CSV ===
desc_df = pd.DataFrame(plot_data)
desc_df.to_csv("data/descriptions/descriptions_all.csv", index=False)

print("📁 All descriptions saved to: data/descriptions/descriptions_all.csv")