import streamlit as st
import pandas as pd
from src.recommender import load_data, get_recommendations
from src.api import fetch_movie_details, fetch_movie_trailer

st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")

def add_bg_and_github_logo():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://i.ibb.co/yNNpczC/slider-bg.jpg");
            background-size: cover;
        }}
        .github-logo {{
            position: absolute;
            top: 3px;
            right: 3px;
            z-index: 1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <a href="https://github.com/priyanshu2k2">
            <img class="github-logo" src="https://i.ibb.co/syNVjS5/pngegg.png" width="40" height="40"/>
        </a>
        """,
        unsafe_allow_html=True
    )

add_bg_and_github_logo()

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        background-color: #FF4B2B;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF416C;
        box-shadow: 0 4px 8px rgba(255, 75, 43, 0.4);
    }
    .metric-card {
        background-color: #2c2c3e;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #FF4B2B;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #aaaaaa;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommendation System")
st.markdown("Powered by Sentence Transformers for deep contextual understanding.")

# Load Data
movies, similarity = load_data()

if movies.empty:
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Controls")
num_recommendations = st.sidebar.slider("Number of recommendations", 3, 10, 5)

# Initialize session state for watchlist
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = set()

# Main Input
selected_movie = st.selectbox(
    "Search for a movie you love:",
    movies['title'].values,
    index=list(movies['title'].values).index("The Dark Knight") if "The Dark Knight" in movies['title'].values else 0
)

if st.button("🔮 Magic Recommend"):
    with st.spinner("Analyzing semantic space and fetching details..."):
        
        # 1. Get Recommendations
        recommendations = get_recommendations(selected_movie, movies, similarity, top_n=num_recommendations)
        
        st.success(f"Found {num_recommendations} incredible matches based on '{selected_movie}'!")
        
        # 2. Display Input Movie Details at the top
        st.markdown("### 🎯 Your Selection")
        input_movie_id = movies[movies['title'] == selected_movie].iloc[0].movie_id
        input_details = fetch_movie_details(input_movie_id)
        
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(input_details['poster_url'], use_container_width=True)
        with col2:
            st.markdown(f"**{input_details['title']}** ({input_details['release_date'][:4] if input_details['release_date'] else 'N/A'})")
            st.markdown(f"*{', '.join(input_details['genres'])}*")
            st.write(input_details['overview'])
            
            # Trailer
            trailer_key = fetch_movie_trailer(input_movie_id)
            if trailer_key:
                with st.expander("Watch Trailer"):
                    st.video(f"https://www.youtube.com/watch?v={trailer_key}")
                    
        st.divider()
        st.markdown("### ✨ AI Recommendations")
        
        # 3. Display Recommendations in a grid
        # Create rows of 5 columns
        cols_per_row = 5
        
        for i in range(0, len(recommendations), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                idx = i + j
                if idx < len(recommendations):
                    rec = recommendations[idx]
                    col = cols[j]
                    
                    details = fetch_movie_details(rec['movie_id'])
                    
                    with col:
                        st.image(details['poster_url'], use_container_width=True)
                        st.markdown(f"**{details['title']}**")
                        
                        # Similarity and Rating metrics
                        m1, m2 = st.columns(2)
                        with m1:
                            st.markdown(f"<div class='metric-card'><div class='metric-value'>{rec['similarity_score']:.2f}</div><div class='metric-label'>Match</div></div>", unsafe_allow_html=True)
                        with m2:
                            st.markdown(f"<div class='metric-card'><div class='metric-value'>{details['rating']:.1f}</div><div class='metric-label'>Rating</div></div>", unsafe_allow_html=True)
                        
                        with st.popover("Details"):
                            st.markdown(f"**Release:** {details['release_date']}")
                            st.markdown(f"**Genres:** {', '.join(details['genres'])}")
                            st.write(details['overview'])
                            if st.button("Add to Watchlist", key=f"add_{rec['movie_id']}"):
                                st.session_state.watchlist.add(details['title'])
                                st.rerun()

# Display Watchlist in sidebar
if st.session_state.watchlist:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Your Watchlist")
    for item in st.session_state.watchlist:
        st.sidebar.markdown(f"- {item}")
    if st.sidebar.button("Clear Watchlist"):
        st.session_state.watchlist.clear()
        st.rerun()
