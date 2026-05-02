import pickle
import pandas as pd
import streamlit as st
import os

# Define absolute paths so this works regardless of where the app is run from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_PATH = os.path.join(BASE_DIR, 'movie_dict.pkl')
SIM_PATH = os.path.join(BASE_DIR, 'similarity.pkl')

@st.cache_data
def load_data():
    """Load the pre-processed movie DataFrame and similarity matrix."""
    try:
        movies_dict = pickle.load(open(DICT_PATH, 'rb'))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open(SIM_PATH, 'rb'))
        return movies, similarity
    except FileNotFoundError as e:
        st.error(f"Data files not found: {e}. Please run the embeddings script first.")
        return pd.DataFrame(), []

def get_recommendations(movie_title, movies_df, similarity_matrix, top_n=5):
    """
    Given a movie title, return the top N similar movies.
    Returns a list of dictionaries with basic movie info.
    """
    if movie_title not in movies_df['title'].values:
        return []

    # Find the index of the movie in the DataFrame
    movie_index = movies_df[movies_df['title'] == movie_title].index[0]
    
    # Get the row of similarity scores for this movie
    movie_similarities = similarity_matrix[movie_index]
    
    # Sort the movies based on similarity scores (descending)
    # enumerate gives us (index, score) pairs
    distances = sorted(list(enumerate(movie_similarities)), reverse=True, key=lambda x: x[1])
    
    recommended_movies = []
    # Skip the first one since it's the movie itself (score of 1.0)
    for i in distances[1:top_n+1]:
        idx = i[0]
        score = i[1]
        recommended_movies.append({
            'movie_id': movies_df.iloc[idx]['movie_id'],
            'title': movies_df.iloc[idx]['title'],
            'similarity_score': score
        })

    return recommended_movies
