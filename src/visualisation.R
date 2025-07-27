# Set working directory to project root
setwd("D:/RA assessment/bollywood-movie-analysis")

# Load required libraries
library(ggplot2)
library(dplyr)
library(tidyr)
library(readr)
library(magrittr)  # for %>% and pipe functionality

# Create output directory if it doesn't exist
if (!dir.exists("data")) dir.create("data")

# Load thematic coding data
df <- read_csv("data/thematic_coding.csv")

# === Plot 1: Time series of theme frequencies by year ===
plot1 <- df %>%
  count(year, theme) %>%
  ggplot(aes(x = year, y = n, color = theme)) +
  geom_line(size = 1.2) +
  labs(title = "Theme Frequency Over Time",
       x = "Year", y = "Count", color = "Theme") +
  theme_minimal()

ggsave("data/theme_frequency.png", plot = plot1, width = 8, height = 5)

# === Plot 2: Sentiment breakdown for each theme ===
plot2 <- df %>%
  count(theme, sentiment_category) %>%
  ggplot(aes(x = theme, y = n, fill = sentiment_category)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Sentiment Categories by Theme",
       x = "Theme", y = "Count", fill = "Sentiment") +
  theme_minimal()

ggsave("data/theme_sentiment_breakdown.png", plot = plot2, width = 8, height = 5)

# === Plot 3: Stacked area chart of theme + sentiment over time ===
plot3 <- df %>%
  count(year, theme, sentiment_category) %>%
  unite("theme_sentiment", theme, sentiment_category, remove = FALSE) %>%
  ggplot(aes(x = year, y = n, fill = theme_sentiment)) +
  geom_area(position = "stack") +
  labs(title = "Stacked Sentiment and Theme Over Time",
       x = "Year", y = "Frequency", fill = "Theme+Sentiment") +
  theme_minimal()

ggsave("data/theme_sentiment_over_time.png", plot = plot3, width = 8, height = 5)

cat("✅ Plots saved in /data/\n")

