import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from loguru import logger
from wordcloud import WordCloud

# Load Data
logger.info("Loading datasets...")
movies_overview = pd.read_csv("data/processed/movies_overview.tsv", sep="\t")
actors_data = pd.read_csv("data/processed/top_actors.tsv", sep="\t")
genre_trends = pd.read_csv("data/processed/genre_trends.tsv", sep="\t")

# Streamlit App
st.title("Movie Data Analysis Dashboard")

# Define and create tabs in Streamlit
tab_names = ['Movie Ratings', 'Actor Popularity', 'User-Movie Preferences']
tabs = st.tabs(tab_names)

with tabs[0]:
    # Filters
    selected_year = st.selectbox("Select Year", sorted(movies_overview["startYear"].unique(), reverse=True))
    filtered_movies = movies_overview[movies_overview["startYear"] == selected_year]

    # Compute Top 10 Movies by Bayesian Average
    if not filtered_movies.empty:
        top_movies = filtered_movies.nlargest(10, "bayesian_avg_rating")

        # Compute summary metrics
        avg_runtime = top_movies["runtimeMinutes"].mean()
        avg_votes = top_movies["numVotes"].mean()

        # Styled container for metrics
        with st.container():
            col1, col2 = st.columns(2)
            col1.metric("⏳ Average Runtime (mins)", f"{avg_runtime:.1f}")
            col2.metric("🗳️ Average Number of Votes", f"{avg_votes:.0f}")

        # Plot Horizontal Bar Chart
        st.subheader(f"Top 10 Highest Rated Movies of {selected_year}")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x=top_movies["bayesian_avg_rating"], y=top_movies["primaryTitle"], palette="viridis", ax=ax)
        ax.set_xlabel("Bayesian Average Rating")
        ax.set_ylabel("Movie Title")
        ax.set_title("Top 10 Highest Rated Movies")
        st.pyplot(fig)

        with st.expander("Tabular Format"):
            st.dataframe(top_movies)

        # Genre Word Cloud
        st.subheader("Genre Word Cloud")

        # Explode the genre column
        genre_df = filtered_movies.assign(genres=filtered_movies["genres"].str.split(",")).explode("genres")

        # Create a frequency dictionary for word cloud
        genre_counts = genre_df["genres"].value_counts().to_dict()

        # Generate the word cloud
        wordcloud = WordCloud(
            width=800, height=400, background_color="white", colormap="viridis"
        ).generate_from_frequencies(genre_counts)

        # Display the word cloud
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")  # Hide axes
        st.pyplot(fig)

    else:
        st.write("No movies found for the selected filters.")

    st.markdown(r"""
    ### Popularity Score Computation:
    $$
    BAR = \frac{v}{v + m} R + \frac{m}{v + m} C
    $$

    where:
    - BAR = Bayesian Average Rating  
    - R = Movie's average rating  
    - v = Number of votes for the movie  
    - m = Minimum votes required (threshold)  
    - C = Global mean rating (average rating across all movies)  

    This formula ensures that movies with very few votes do not dominate the rankings by balancing individual ratings with the overall dataset.
    """)

       
with tabs[1]:
    # Filters
    selected_year_actor = st.selectbox("Select Year", sorted(actors_data["startYear"].unique(), reverse=True), key="selected_year_actor")
    selected_metric = st.radio(
        "Select Popularity Metric",
        ["Total Movies", "Total Votes", "Popularity Score"],
        key="actor_metric"
    )
    # Filter data by selected year
    filtered_actor = actors_data[actors_data["startYear"] == selected_year_actor]

    # Compute Metrics
    if selected_metric == "Total Movies":
        top_actors =  filtered_actor.groupby("primaryName")["num_movies"].sum().nlargest(10).reset_index()
        metric_col = "num_movies"
        xlabel = "Number of Movies"
    elif selected_metric == "Total Votes":
        top_actors =  filtered_actor.groupby("primaryName")["total_votes"].sum().nlargest(10).reset_index()
        metric_col = "total_votes"
        xlabel = "Total Votes"
    else:  # Popularity Score
        top_actors =  filtered_actor.groupby("primaryName")["popularity_score"].mean().nlargest(10).reset_index()
        metric_col = "popularity_score"
        xlabel = "Popularity Score"

    # Plot Horizontal Bar Chart
    if not top_actors.empty:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x=top_actors[metric_col], y=top_actors["primaryName"], palette="coolwarm", ax=ax)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Actor Name")
        ax.set_title(f"Top 10 Actors by {selected_metric}")
        st.pyplot(fig)
    else:
        st.write("No actors found for the selected filters.")

    # Computation Formulas in LaTeX
    st.markdown(r"""
        ### Popularity Score Computation:
        $$
        \text{popularity\_score}_i = (0.4 \times \text{actor\_counts\_norm}_i) + (0.4 \times \text{actor\_total\_votes\_norm}_i) + (0.2 \times \text{knowntitle\_count}_i)
        $$

        where:
        
        -  $$ \text{actor\_counts\_norm}_i $$ is the normalized count of movies for actor \( i \).
        - $$\text{actor\_total\_votes\_norm}_i $$is the normalized total votes for actor \( i \).
        - $$ \text{knowntitle\_count}_i $$ is the sum of titles that the actor is known for\( i \).

        This formula ensures a balanced ranking based on an actor’s number of movies, audience engagement, and count of known roles.
        """)
    
with tabs[2]:
   # Select year range using a slider
    min_year, max_year = int(genre_trends["startYear"].min()), int(genre_trends["startYear"].max())
    selected_year_range = st.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(2000, 2025)  # Default range: 2000-2025
    )

    st.subheader(f"Genre Distribution Heatmap ({selected_year_range[0]} - {selected_year_range[1]})")

    # Filter genre_trends based on the selected year range
    filtered_genre_data = genre_trends[
        (genre_trends["startYear"] >= selected_year_range[0]) & 
        (genre_trends["startYear"] <= selected_year_range[1])
    ]

    # Aggregate total movies per genre per year
    genre_trend_counts = filtered_genre_data.groupby(["startYear", "genres"])["num_movies"].sum().reset_index()

    # Pivot table: Years as index, Genres as columns
    genre_trend_pivot = genre_trend_counts.pivot(index="startYear", columns="genres", values="num_movies").fillna(0)

    # Heatmap of genre distribution
    plt.figure(figsize=(12, 6))
    sns.heatmap(genre_trend_pivot.T, cmap="viridis", linewidths=0.5)
    plt.ylabel("Genres")  
    plt.xlabel("Year")   
    st.pyplot(plt)
    plt.clf()  

    # Average Movie Runtime Over Time
    st.subheader(f"Average Movie Runtime Over Time ({selected_year_range[0]} - {selected_year_range[1]})")

    # Filter movies_overview for the selected year range
    filtered_movies = movies_overview[
        (movies_overview["startYear"] >= selected_year_range[0]) & 
        (movies_overview["startYear"] <= selected_year_range[1])
    ]

    # Compute average runtime per year
    runtime_trends = filtered_movies.groupby("startYear")["runtimeMinutes"].mean().dropna()

    # Line graph of average runtime per year
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=runtime_trends.index, y=runtime_trends.values, marker="o")
    plt.xlabel("Year")
    plt.ylabel("Runtime (minutes)")
    plt.grid(True)  
    st.pyplot(plt)
    plt.clf() 

   