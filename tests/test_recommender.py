import pytest
import pandas as pd
import numpy as np
from src.recommender import get_recommendations

@pytest.fixture
def dummy_data():
    """Create a dummy movie dataframe and similarity matrix for testing."""
    movies_df = pd.DataFrame({
        'movie_id': [1, 2, 3, 4],
        'title': ['Action Movie', 'Comedy Movie', 'Another Action', 'Drama Movie'],
        'tags': ['action explosions', 'funny laughs', 'action guns', 'sad tears']
    })
    
    # Fake similarity matrix (Action Movie is most similar to Another Action)
    similarity_matrix = np.array([
        [1.0, 0.1, 0.9, 0.0],  # Action Movie
        [0.1, 1.0, 0.2, 0.0],  # Comedy Movie
        [0.9, 0.2, 1.0, 0.0],  # Another Action
        [0.0, 0.0, 0.0, 1.0]   # Drama Movie
    ])
    
    return movies_df, similarity_matrix

def test_get_recommendations_returns_correct_number(dummy_data):
    movies_df, similarity_matrix = dummy_data
    # Request top 2
    recs = get_recommendations('Action Movie', movies_df, similarity_matrix, top_n=2)
    assert len(recs) == 2

def test_get_recommendations_excludes_input_movie(dummy_data):
    movies_df, similarity_matrix = dummy_data
    recs = get_recommendations('Action Movie', movies_df, similarity_matrix, top_n=3)
    titles = [r['title'] for r in recs]
    assert 'Action Movie' not in titles

def test_get_recommendations_sorts_correctly(dummy_data):
    movies_df, similarity_matrix = dummy_data
    recs = get_recommendations('Action Movie', movies_df, similarity_matrix, top_n=3)
    
    # The most similar movie to 'Action Movie' is 'Another Action' (score 0.9)
    assert recs[0]['title'] == 'Another Action'
    assert recs[0]['similarity_score'] == 0.9

def test_get_recommendations_handles_unknown_movie(dummy_data):
    movies_df, similarity_matrix = dummy_data
    recs = get_recommendations('Unknown Movie', movies_df, similarity_matrix, top_n=3)
    assert len(recs) == 0
