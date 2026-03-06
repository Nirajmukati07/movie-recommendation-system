<<<<<<< HEAD
from fastapi import FastAPI
import pandas as pd
import difflib
from fastapi.middleware.cors import CORSMiddleware
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
selected_features = ['genres','keywords','tagline','cast','director']

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
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

# Similarity matrix
similarity = cosine_similarity(feature_vectors)


def recommend(movie_name):

    list_of_movies = movies_data['title'].tolist()

    find_close_match = difflib.get_close_matches(movie_name, list_of_movies)

    if not find_close_match:
        return ["Movie not found"]

    close_match = find_close_match[0]

    index_of_movie = movies_data[movies_data.title == close_match].index[0]

    similarity_score = list(enumerate(similarity[index_of_movie]))

    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommended_movies = []

    for movie in sorted_similar_movies[1:21]:
        index = movie[0]
        title = movies_data.iloc[index].title
        recommended_movies.append(title)

    return recommended_movies


@app.get("/recommend/{movie}")
def get_recommendations(movie: str):
=======
from fastapi import FastAPI
import pandas as pd
import difflib
from fastapi.middleware.cors import CORSMiddleware
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
selected_features = ['genres','keywords','tagline','cast','director']

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
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

# Similarity matrix
similarity = cosine_similarity(feature_vectors)


def recommend(movie_name):

    list_of_movies = movies_data['title'].tolist()

    find_close_match = difflib.get_close_matches(movie_name, list_of_movies)

    if not find_close_match:
        return ["Movie not found"]

    close_match = find_close_match[0]

    index_of_movie = movies_data[movies_data.title == close_match].index[0]

    similarity_score = list(enumerate(similarity[index_of_movie]))

    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommended_movies = []

    for movie in sorted_similar_movies[1:21]:
        index = movie[0]
        title = movies_data.iloc[index].title
        recommended_movies.append(title)

    return recommended_movies


@app.get("/recommend/{movie}")
def get_recommendations(movie: str):
>>>>>>> f495ca5afcb06abc29e8acfda63b0e5322580cef
    return {"recommendations": recommend(movie)}