# IMDb dataset file paths
IMDB_DATA_PATH = "data/raw/"

imdb_files = {
    "title_akas": "title.akas.tsv",
    "title_basics": "title.basics.tsv",
    "title_crew": "title.crew.tsv",
    "title_episode": "title.episode.tsv",
    "title_principals": "title.principals.tsv",
    "title_ratings": "title.ratings.tsv",
    "name_basics": "name.basics.tsv"
}

# Define data types for each dataset
dtypes = {
    "title_akas": {
        "titleId": "string",
        "ordering": "Int64",
        "title": "string",
        "region": "string",
        "language": "string",
        "types": "string",
        "attributes": "string",
        "isOriginalTitle": "boolean"
    },
    "title_basics": {
        "tconst": "string",
        "titleType": "string",
        "primaryTitle": "string",
        "originalTitle": "string",
        "isAdult": "boolean",
        "startYear": "Int64",
        "endYear": "Int64",
        "runtimeMinutes": "Int64",
        "genres": "string"
    },
    "title_crew": {
        "tconst": "string",
        "directors": "string",
        "writers": "string"
    },
    "title_episode": {
        "tconst": "string",
        "parentTconst": "string",
        "seasonNumber": "Int64",
        "episodeNumber": "Int64"
    },
    "title_principals": {
        "tconst": "string",
        "ordering": "Int64",
        "nconst": "string",
        "category": "string",
        "job": "string",
        "characters": "string"
    },
    "title_ratings": {
        "tconst": "string",
        "averageRating": "float64",
        "numVotes": "Int64"
    },
    "name_basics": {
        "nconst": "string",
        "primaryName": "string",
        "birthYear": "Int64",
        "deathYear": "Int64",
        "primaryProfession": "string",
        "knownForTitles": "string"
    }
}