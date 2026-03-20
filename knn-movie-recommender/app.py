import streamlit as st
from model import load_recommender

# Load cached model
recommender = load_recommender()

st.title("🎬 Movie Recommender System (KNN)")

user_id = st.number_input("Enter User ID", min_value=1, step=1)

if st.button("Recommend Movies"):
    try:
        recs = recommender.recommend_movies(user_id)
        st.subheader("Recommended Movies:")
        for movie in recs:
            st.write("👉", movie)
    except ValueError:
        st.error("User not found. Try another ID.")