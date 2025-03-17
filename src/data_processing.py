import pandas as pd
import numpy as np
import os
from loguru import logger
from data_fetching import load_imdb_data  # Function to load data

# Define output directory
output_dir = "data/processed"
os.makedirs(output_dir, exist_ok=True)
logger.info(f"Output directory set to: {output_dir}")

# ---------------------------
# 1️ Create movies_overview
# ---------------------------
logger.info("Loading title_basics and title_ratings...")
title_basics = load_imdb_data("title_basics")
title_ratings = load_imdb_data("title_ratings")

# Filter only movies and TV movies
title_basics = title_basics[title_basics["titleType"].isin(["movie", "tvMovie"])]

logger.info("Merging title_basics and title_ratings...")
movies_overview = title_basics.merge(title_ratings, on="tconst", how="inner")[
    ["tconst", "primaryTitle", "startYear", "runtimeMinutes", "genres", "averageRating", "numVotes"]
]

# Compute Bayesian Average Rating
m = 1025  # Minimum number of votes required
C = movies_overview["averageRating"].mean()  # Global mean rating
movies_overview["bayesian_avg_rating"] = (
    (movies_overview["numVotes"] / (movies_overview["numVotes"] + m) * movies_overview["averageRating"]) +
    (m / (movies_overview["numVotes"] + m) * C)
)

# Remove null values
movies_overview = movies_overview.dropna()
logger.info("Dropped null values from movies_overview")

movies_overview.to_csv(f"{output_dir}/movies_overview.tsv", sep="\t", index=False)
logger.info("Saved movies_overview.tsv")

# ---------------------------
# 2 Create top_actors
# ---------------------------
logger.info("Loading title_principals, name_basics, and movies_overview...")

title_principals = load_imdb_data("title_principals")
name_basics = load_imdb_data("name_basics")

# Merge actors with movies and filter only actors/actresses
actors = title_principals.merge(movies_overview, on="tconst", how="inner")
actors = actors[actors["category"].isin(["actor", "actress"])]

# Merge actors with name_basics to get actor names
actors = actors.merge(name_basics[["nconst", "primaryName", "knownForTitles"]], on="nconst", how="left")

# Extract startYear from movies
actors = actors[["nconst", "primaryName", "tconst", "numVotes", "startYear", "knownForTitles"]]

# Compute actor-level statistics per year
logger.info("Aggregating actor statistics...")
top_actors = actors.groupby(["nconst", "primaryName", "startYear"], as_index=False).agg(
    num_movies=("tconst", "count"),
    total_votes=("numVotes", "sum"),
    known_titles_count=("knownForTitles", lambda x: x.str.split(',').str.len().sum())  
)

# Normalize features within each year
logger.info("Computing normalized popularity metrics...")
top_actors["actor_counts_norm"] = top_actors.groupby("startYear")["num_movies"].transform(lambda x: x / x.max())
top_actors["actor_total_votes_norm"] = top_actors.groupby("startYear")["total_votes"].transform(lambda x: x / x.max())
top_actors["known_titles_norm"] = top_actors.groupby("startYear")["known_titles_count"].transform(lambda x: x / x.max())

# Compute popularity score
top_actors["popularity_score"] = (top_actors["actor_counts_norm"] * 0.4) + \
                                 (top_actors["actor_total_votes_norm"] * 0.4) + \
                                 (top_actors["known_titles_norm"] * 0.2)

# Save to output directory
top_actors.to_csv(f"{output_dir}/top_actors.tsv", sep="\t", index=False)
logger.info("Saved top_actors.tsv")

# ---------------------------
# 3 Create genre_trends
# ---------------------------
logger.info("Processing genre trends...")
exploded_genres = title_basics.copy()
exploded_genres["genres"] = exploded_genres["genres"].str.split(",")
exploded_genres = exploded_genres.explode("genres")

# Aggregate by year and genre
logger.info("Aggregating genre data...")
genre_trends = exploded_genres.merge(title_ratings, on="tconst", how="inner").groupby(["startYear", "genres"]).agg(
    num_movies=("tconst", "count"),
    avg_rating=("averageRating", "mean"),
    total_votes=("numVotes", "sum")
).reset_index()

# Remove null values
genre_trends = genre_trends.dropna()
logger.info("Dropped null values from genre_trends dataset")

genre_trends.to_csv(f"{output_dir}/genre_trends.tsv", sep="\t", index=False)
logger.info("Saved genre_trends.tsv")

# ---------------------------
# 4 Create aaa_movie_candidates
# ---------------------------
logger.info("Loading title_crew...")
title_crew = load_imdb_data("title_crew")

aaa_movies = movies_overview.merge(title_crew, on="tconst", how="left")[
    ["tconst", "primaryTitle", "startYear", "genres", "averageRating", "numVotes"]
]

# Remove null values
aaa_movies = aaa_movies.dropna()
logger.info("Dropped null values from aaa_movie_candidates dataset")

# Compute AAA Score
logger.info("Computing AAA scores...")
aaa_movies["aaa_score"] = (aaa_movies["averageRating"] * np.log1p(aaa_movies["numVotes"])) / (1 + np.exp(-(2025 - aaa_movies["startYear"])))

aaa_movies.to_csv(f"{output_dir}/aaa_movie_candidates.tsv", sep="\t", index=False)
logger.info("Saved aaa_movie_candidates.tsv")

logger.info("All TSV files successfully saved.")
