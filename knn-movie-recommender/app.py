import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Load data
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# Create matrix
movie_matrix = ratings.pivot_table(
    index='userId',
    columns='movieId',
    values='rating'
).fillna(0)

# Train model
model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(movie_matrix)

# Functions
def find_similar_users(user_id, k=5):
    user_vector = movie_matrix.loc[user_id].values.reshape(1, -1)
    distances, indices = model.kneighbors(user_vector, n_neighbors=k+1)
    return indices.flatten()[1:]

def recommend_movies(user_id, num_recommendations=5):
    similar_users = find_similar_users(user_id)

    user_movies = movie_matrix.loc[user_id]
    watched_movies = user_movies[user_movies > 0].index

    recommendations = {}

    for sim_user in similar_users:
        sim_user_ratings = movie_matrix.iloc[sim_user]

        for movie_id, rating in sim_user_ratings.items():
            if movie_id not in watched_movies and rating > 3:
                recommendations[movie_id] = recommendations.get(movie_id, 0) + rating

    sorted_movies = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
    top_movies = [movie[0] for movie in sorted_movies[:num_recommendations]]

    return movies[movies['movieId'].isin(top_movies)]['title'].tolist()

# UI
st.title("🎬 Movie Recommender System (KNN)")

user_id = st.number_input("Enter User ID", min_value=1, step=1)

if st.button("Recommend Movies"):
    try:
        recs = recommend_movies(user_id)

        st.subheader("Recommended Movies:")
        for movie in recs:
            st.write("👉", movie)

    except:
        st.error("User not found. Try another ID.")