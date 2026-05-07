from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset
movies_data = pd.read_csv("movies.csv")

# Select relevant features
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']

# Fill missing values
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

# Combine features
combined_features = (
    movies_data['genres'] + ' ' +
    movies_data['keywords'] + ' ' +
    movies_data['tagline'] + ' ' +
    movies_data['cast'] + ' ' +
    movies_data['director']
)

# Convert text → vectors
vectorizer = TfidfVectorizer(stop_words='english')
feature_vectors = vectorizer.fit_transform(combined_features)

# Similarity matrix
similarity = cosine_similarity(feature_vectors)


def get_movie_details(index: int) -> dict:
    row = movies_data.iloc[index]
    return {
        "title": row.title,
        "tagline": row.tagline if pd.notna(row.tagline) else "",
        "overview": row.overview if pd.notna(row.overview) else "",
        "genres": row.genres if pd.notna(row.genres) else "",
        "release_date": row.release_date if pd.notna(row.release_date) else "",
        "vote_average": row.vote_average if pd.notna(row.vote_average) else "",
        "director": row.director if pd.notna(row.director) else "",
        "cast": row.cast if pd.notna(row.cast) else "",
    }


def recommend(movie_name: str) -> list:
    list_of_movies = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_movies, n=1, cutoff=0.5)

    if not find_close_match:
        return []

    close_match = find_close_match[0]
    index_of_movie = movies_data[movies_data.title == close_match].index[0]

    similarity_score = list(enumerate(similarity[index_of_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommended_movies = []
    for movie in sorted_similar_movies[1:21]:
        index = movie[0]
        recommended_movies.append(get_movie_details(index))

    return recommended_movies


@app.get("/suggest")
def suggest_titles(query: str = Query(..., min_length=1)):
    query_lower = query.lower()
    matches = movies_data[movies_data['title'].str.lower().str.contains(query_lower, na=False)]
    suggestions = matches['title'].head(10).tolist()

    if not suggestions:
        suggestions = difflib.get_close_matches(query, movies_data['title'].tolist(), n=10, cutoff=0.3)

    return {"results": suggestions}


@app.get("/recommend")
def get_recommendations(movie: str = Query(..., min_length=1)):
    recommendations = recommend(movie)
    if not recommendations:
        return {"recommendations": [], "message": "Movie not found. Try a different title."}
    return {"recommendations": recommendations}
