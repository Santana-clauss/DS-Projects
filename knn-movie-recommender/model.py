import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import streamlit as st

class MovieRecommender:
    def __init__(self, movies_path="data/movies.csv", ratings_path="data/ratings.csv"):
        # Load data
        self.movies = pd.read_csv(movies_path)
        self.ratings = pd.read_csv(ratings_path)

        # Create user-movie matrix
        self.movie_matrix = self.ratings.pivot_table(
            index='userId',
            columns='movieId',
            values='rating'
        ).fillna(0)

        # Train KNN model
        self.model = NearestNeighbors(metric='cosine', algorithm='brute')
        self.model.fit(self.movie_matrix)

    def find_similar_users(self, user_id, k=5):
        if user_id not in self.movie_matrix.index:
            raise ValueError("User not found")
        user_vector = self.movie_matrix.loc[user_id].values.reshape(1, -1)
        distances, indices = self.model.kneighbors(user_vector, n_neighbors=k+1)
        return indices.flatten()[1:]

    def recommend_movies(self, user_id, num_recommendations=5):
        similar_users = self.find_similar_users(user_id)
        user_movies = self.movie_matrix.loc[user_id]
        watched_movies = user_movies[user_movies > 0].index

        recommendations = {}
        for sim_user in similar_users:
            sim_user_ratings = self.movie_matrix.iloc[sim_user]
            for movie_id, rating in sim_user_ratings.items():
                if movie_id not in watched_movies and rating > 3:
                    recommendations[movie_id] = recommendations.get(movie_id, 0) + rating

        sorted_movies = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        top_movies = [movie[0] for movie in sorted_movies[:num_recommendations]]

        return self.movies[self.movies['movieId'].isin(top_movies)]['title'].tolist()


# Streamlit cache
@st.cache_resource
def load_recommender():
    return MovieRecommender()