# 🎬 Movie Recommendation System

![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B2B.svg)
![Sentence Transformers](https://img.shields.io/badge/Sentence_Transformers-2.5-green.svg)

This is a portfolio-grade, content-based movie recommendation engine. It goes beyond simple keyword matching by using deep learning (**Sentence Transformers**) to understand the semantic meaning of movie plots, genres, and metadata, providing highly accurate and intelligent recommendations.

## ✨ Features

- **🧠 Semantic AI Search**: Powered by `all-MiniLM-L6-v2` for deep contextual recommendations.
- **🔥 Trending Movies**: Real-time trending data fetched via the TMDB API.
- **🎥 Deep Movie Details**: View posters, ratings, release years, overviews, and embedded YouTube trailers.
- **📋 Watchlist**: Save movies to your session watchlist.
- **📊 Analytics Dashboard**: Visualize dataset distributions, tag lengths, and keyword frequencies.

## 🏗️ Architecture

1. **Data**: The TMDB 5000 Movies Dataset.
2. **Embedding**: The `tags` (combined genres, cast, crew, and overview) are passed through an LLM to generate 384-dimensional dense vectors.
3. **Similarity**: A cosine similarity matrix is computed and saved as `similarity.pkl`.
4. **Application**: A multi-page Streamlit app serves the frontend, dynamically fetching live posters and trailers from the TMDB API.

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Movie-Recommendation-System.git
   cd Movie-Recommendation-System
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate the ML Model:**
   This step computes the semantic embeddings. It only needs to be run once.
   ```bash
   python scripts/compute_embeddings.py
   ```

4. **Run the App:**
   ```bash
   streamlit run app.py
   ```

## 🐳 Docker Support

To run the application using Docker:

```bash
docker build -t valura-movies .
docker run -p 8501:8501 valura-movies
```

## 🧪 Testing

To run the test suite:
```bash
pytest tests/
```
