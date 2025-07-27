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
    - Additional plots illustrate further nuances and comparisons, all available in the `plots/` directory.
- **Reproducibility**: All R scripts required to recreate these analyses from the CSVs are provided.

---

## Repository Structure
bollywood-movie-analysis/
│
├── data/
│ ├── subtitles/
│ ├── descriptions/
│ ├── posters/
│ └── sampled_movies.csv
│
├── scripts/
│ └── sample_movies.py/.ipynb # Script for sampling movies
│
├── notebooks/
│ └── analysis.ipynb # Notebooks for EDA and theme coding
│
├── plots/
│ ├── theme_time_series.png
│ └── [other-plot].png
│
├── sentiment_data.csv # Main thematic/sentiment-coded data
├── supplementary_ideas.md # Additional ideas, limitations, and notes
├── README.md # This file


---

## Key Design Principles

- **Transparency & Reproducibility**: All steps from data acquisition to analysis are scripted or documented for easy reruns by others.
- **AI Integration**: LLMs are used for scalable, auditable sentiment and theme classification, with logic and categories documented.
- **Extensibility**: Modular folder and code structure allow for easy addition of new movies, themes, or coding improvements.

---

## Using This Repo

1. **Data Access**: Some raw data (e.g., Kaggle datasets, subtitles) may need to be downloaded manually due to copyright. Follow instructions in `scripts/` and `notebooks/`.
2. **Re-analysis**: To resample, run the sampling script. For (re)coding or sentiment analysis, use the LLM-powered scripts/notebooks with the `subtitles_all.csv` and `descriptions_all.csv`as reference.
3. **Plotting**: Open R scripts or notebooks and run analyses on the included `.csv` files for instant visual output.

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