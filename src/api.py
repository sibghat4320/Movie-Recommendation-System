import os
import requests
import streamlit as st

# Try to get API key from environment or secrets, fallback to default
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
if not TMDB_API_KEY:
    try:
        TMDB_API_KEY = st.secrets.get("TMDB_API_KEY")
    except Exception:
        # Fallback if secrets.toml doesn't exist
        TMDB_API_KEY = None

if not TMDB_API_KEY:
    st.error("TMDB_API_KEY not found. Please set it in environment variables or secrets.toml")

@st.cache_data(show_spinner=False, ttl=86400)
def fetch_movie_details(movie_id):
    """Fetch complete movie details including poster, rating, overview, genres."""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        poster_path = data.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"
        
        # Extract genres safely
        genres = [g.get('name') for g in data.get('genres', [])]
        
        return {
            'title': data.get('title', 'Unknown Title'),
            'poster_url': poster_url,
            'overview': data.get('overview', 'No overview available.'),
            'rating': data.get('vote_average', 0.0),
            'release_date': data.get('release_date', 'Unknown'),
            'genres': genres,
            'runtime': data.get('runtime', 0),
            'tagline': data.get('tagline', ''),
            'homepage': data.get('homepage', '')
        }
    except Exception as e:
        print(f"Error fetching movie {movie_id}: {e}")
        return {
            'title': 'Error',
            'poster_url': "https://via.placeholder.com/500x750?text=Error",
            'overview': 'Failed to load details.',
            'rating': 0.0,
            'release_date': 'Unknown',
            'genres': [],
            'runtime': 0,
            'tagline': '',
            'homepage': ''
        }

@st.cache_data(show_spinner=False, ttl=86400)
def fetch_movie_trailer(movie_id):
    """Fetch YouTube trailer key for a movie."""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        for video in data.get('results', []):
            if video.get('site') == 'YouTube' and video.get('type') == 'Trailer':
                return video.get('key')
        return None
    except Exception:
        return None

@st.cache_data(show_spinner=False, ttl=3600)
def fetch_trending_movies():
    """Fetch current trending movies for the homepage."""
    try:
        url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])[:10]  # Return top 10
    except Exception:
        return []
