# Bollywood Movie Analysis Project

## Project Overview

The objective of this project is to curate and analyze a **dataset of Indian movies (post-2010 releases)** in order to study how themes such as Hindu–Muslim relations, gender relations, and nationalism are depicted over time, using reproducible and transparent data science best practices.

---

## Pipeline Breakdown

### 1. Dataset Download & Sampling

- **Source**: The Indian Movie Database from Kaggle (<https://www.kaggle.com/datasets/pncnmnp/the-indian-movie-database>).
- **Sampling**: Selected a random sample of 100 movies released after 2010, preserving all available attributes for each.
    - **Reproducibility**: Sampling is handled by a script located in the `scripts/` folder, which allows others to reproduce or modify the sampling process using the same random seed or parameters.
    - **Data Storage**: The sampled movies are saved as a CSV within the `data/` directory.

### 2. Movie Materials Collection

For each film in the sample, the following are collected and organized:
- **English subtitles** (`data/subtitles/`): Obtained from OpenSubtitles via API.
- **Description/Synopsis** (`data/descriptions/`): Fetched from OMDb using API queries to ensure rich summaries.
- **Movie Posters** (`data/posters/`): Downloaded via TMDb API.

All files maintain a consistent directory structure for ease of navigation and reproducibility.

### 3. Descriptive Metadata & Thematic Coding

- **Manual & Automated Coding**: Both human and LLM (Large Language Model)-based analyses were conducted on subtitle and description text to identify and categorize:
    - *Hindu–Muslim relations*
    - *Gender relations*
    - *Nationalism*
- **Sentiment Classification**: LLMs (e.g., Google Gemini API) are used to not only detect the presence of these themes, but also their sentiment and nuance:
    - Assigned classifications: *Exclusionary vs. Secular (Inclusive)*, *Positive or Negative*, *Progressive or Conservative*.
- 
### 4. Analytical and Visualization Outputs

- **Visualization (R/GGPlot)**: Thematic codes and sentiment labels are visualized in R using ggplot2.
    - Main plot: Annual trends (from 2010 onward) in the frequency and sentiment of each coded theme.
    - Additional plots illustrate further nuances and comparisons, all available in the `data/` directory.
- **Reproducibility**: All R scripts required to recreate these analyses from the CSVs are provided.

---
```
## Repository Structure
bollywood-movie-analysis/
│
├── data/
│ ├── descriptions
│ │ └── descriptions_all.csv   
│ ├── metadata/
│ │ └── metadata_extended.csv
│ ├── posters/
│ │ └── posters_all.csv 
│ ├── sampled/
│ │ └── movies_sampled.csv 
│ ├── subtitles/
│ │ └── subtitles_all.csv
│ ├── bollywood_2010-2019.csv
│ ├── bollywood_meta_2010-2019.csv
│ ├── bollywood_ratings_2010-2019.csv
│ ├── bollywood_text_2010-2019.csv
│ ├── bollywood_coding_clean.csv
│ ├── bollywood_coding.csv
│ ├── theme_frequency.png
│ ├── theme_sentiment_breakdown.png
│ ├── theme_sentiment_overtime.png
│ └── violence_measure.csv
│
├── scripts/
│ ├── description.py 
│ ├── metadata.py 
│ ├── poster.py
│ ├── proposed_sentiment.py
│ ├── sampled_movies.py
│ ├── subtitles.py
│ ├── thematic_clean.py
│ ├── thematic_coding.py  
│ └── visualisation.R 
│
├── supplementary_ideas.md 
├── requirements.txt # Python dependencies
├── requiremnet_r.txt # R dependencies
├── .gitignore
├── .gitattributes
├── .Rprofile
├── LICENSE
├── pdf_coverter.py
├── final_report.html
├── final_report.pdf
├── renv.lock
├── renv/ # R virtual environment
├── venv/ # Python virtual environment
└── README.md 
```

---

  ## How to Run This Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Econbee007/bollywood-movie-analysis.git
cd bollywood-movie-analysis

```

### 2. Setup Python Environment
python -m venv venv
source venv/Scripts/activate  # On Windows
### Or on Mac/Linux: source venv/bin/activate

pip install -r requirements.txt


### 3. Download Full Dataset from Kaggle
Visit: https://www.kaggle.com/datasets/pncnmnp/the-indian-movie-database
Place the files as data/.

### 4. Sample 100 Movies
```bash
python scripts/sampled_movies.py

Output: data/sampled/movies_sampled.csv
```
### 5. Collect Subtitles, Descriptions, and Posters
```bash
python src/subtitles.py
python src/description.py
python src/poster.py

Output: data/subtitles/subtitles_all.csv
        data/descriptions/descriptions_all.csv
        data/posters/posters_all.csv

For subtitles, descriptions and posters the scripts uses OpenSubtitles API, OMDb API, and TMDb API respectively. Before running these scripts, make sure you generate and configure your API keys in a `.env` file in `src/.env`.
```

### 6. Perform Thematic Coding using LLM
```bash
python src/thematic_coding.py 

Output: data/thematic_coding.csv

Now to clean this data use
```bash 
python src/thematic_coding_clean.py

Output: data/thematic_coding_clean.csv
This is the final output for thematic coding.
```
### Themes:
1. Hindu–Muslim relations
2. Gender relations
3. Nationalism
### Sentiment attributes:
1. Exclusionary ↔ Inclusive
2. Positive ↔ Negative
3. Progressive ↔ Conservative

### Additional Thematic Measure: Violence Representation

Now I have proposed a simple sentiment measure in proposed_sentiment.py
The theme here is violence in movies. To complement the core themes, we introduce a new variable: violence_representation, which classifies movie content as "High", "Low", or "Unclear" based on the frequency of violence-related keywords (e.g., kill, gun, riot, bomb) in subtitles and descriptions. This heuristic captures the presence and intensity of violent themes in a reproducible way. While simplistic, it provides a scalable proxy for thematic violence, useful for studying genre, political narratives, or changes over time.

Output: data/violence_measure

### 7. Visualize Trends using R
Run the visualisation.R in your local machine after installing all the requirement_r.txt, you will get the outputs in .png format in data/

## Key Design Principles

- **Transparency & Reproducibility**: All steps from data acquisition to analysis are scripted or documented for easy reruns by others.
- **AI Integration**: LLMs are used for scalable, auditable sentiment and theme classification, with logic and categories documented.
- **Extensibility**: Modular folder and code structure allow for easy addition of new movies, themes, or coding improvements.

---

## Supplementary Notes

- Consult `supplementary_ideas.md` for scalability strategies, known biases, and reflective notes on execution.
- All steps and code are kept modular for maintainability and auditor-friendly workflows.

---

## License

MIT License.

---

This repo is intended as a transparent and extensible resource for researchers, collaborators, and reviewers engaged in AI-powered media analytics in Bollywood cinema.

---
