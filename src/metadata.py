import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from genderize import Genderize  

# --- Load TMDb key ---
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY missing in .env")

# --- Load sample movies ---
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
df = pd.read_csv(os.path.join(PROJECT_DIR, "data", "sampled", "movies_sampled.csv"))

records = []

for _, row in df.iterrows():
    imdb_id = row.get("imdb_id")
    title = row.get("original_title")

    if not imdb_id:
        continue

    # 1. Fetch TMDb movie (+ credits)
    url = f"https://api.themoviedb.org/3/find/{imdb_id}"
    resp = requests.get(url, params={"api_key": TMDB_API_KEY, "external_source": "imdb_id"})
    movie = resp.json().get("movie_results", [])
    if not movie:
        continue
    tmdb_id = movie[0]["id"]

    details = requests.get(
        f"https://api.themoviedb.org/3/movie/{tmdb_id}",
        params={"api_key": TMDB_API_KEY, "append_to_response": "credits"}
    ).json()

    # Director info
    director = next((c for c in details.get("credits", {}).get("crew", []) if c.get("job") == "Director"), {})
    gender_code = director.get("gender", 0)
    gender = {1: "female", 2: "male"}.get(gender_code, None)

    # Fallback name-based gender inference
    if not gender and director.get("name"):
        iso = Genderize().get([director["name"]])[0]
        gender = iso["gender"]

    # 2. Attempt box office via Wikipedia scraping
    wiki = row.get("wiki_link")
    box_office = None
    if isinstance(wiki, str):
        try:
            resp2 = requests.get(wiki)
            soup = BeautifulSoup(resp2.text, "html.parser")
            header = soup.find(lambda tag: tag.name == "th" and "Box office" in tag.text)
            if header:
                val = header.find_next_sibling("td").text.strip()
                box_office = val.replace("\n", " ")
        except Exception:
            box_office = None

    records.append({
        "imdb_id": imdb_id,
        "title": title,
        "director": director.get("name"),
        "director_gender": gender,
        "box_office": box_office or ""
    })

    time.sleep(1.5)

# Save to CSV
out = os.path.join(PROJECT_DIR, "data", "metadata", "metadata_extended.csv")
os.makedirs(os.path.dirname(out), exist_ok=True)
pd.DataFrame(records).to_csv(out, index=False)
print("✅ Extended metadata saved:", out)
