"""
This script computes state-of-the-art semantic embeddings for movies using Sentence Transformers.
It reads the `movie_dict.pkl` file, extracts the 'tags' column, and uses an LLM-based encoder
to create a high-quality similarity matrix, replacing the old CountVectorizer approach.
"""

import os
import pickle
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time

def compute_embeddings():
    print("Starting Machine Learning Upgrade: Semantic Embeddings")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dict_path = os.path.join(base_dir, 'movie_dict.pkl')
    out_path = os.path.join(base_dir, 'similarity.pkl')

    if not os.path.exists(dict_path):
        print(f"Error: Could not find {dict_path}")
        return

    # 1. Load Data
    print("1. Loading movie data...")
    movies_dict = pickle.load(open(dict_path, 'rb'))
    movies = pd.DataFrame(movies_dict)
    print(f"   Found {len(movies)} movies.")

    # 2. Load Model
    print("\n2. Downloading/Loading Sentence Transformer model (all-MiniLM-L6-v2)...")
    print("   This might take a minute on first run...")
    start_time = time.time()
    
    # We use a fast, lightweight, highly effective model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"   Model loaded in {time.time() - start_time:.2f} seconds.")

    # 3. Compute Embeddings
    print("\n3. Computing semantic embeddings for all movie tags...")
    print("   This leverages deep learning to understand context, not just keyword matching.")
    start_time = time.time()
    
    # Extract tags as a list of strings
    texts = movies['tags'].tolist()
    
    # Encode them into high-dimensional vectors
    # show_progress_bar is nice but might not render perfectly in all terminals, so we use print statements
    embeddings = model.encode(texts, batch_size=64, show_progress_bar=True)
    print(f"   Embeddings computed in {time.time() - start_time:.2f} seconds.")

    # 4. Compute Similarity Matrix
    print("\n4. Calculating cosine similarity matrix...")
    start_time = time.time()
    
    # Compute similarity between all pairs (results in a 4806 x 4806 matrix)
    # The output is cast to float16 to save disk space and RAM, reducing 180MB -> 45MB
    similarity = cosine_similarity(embeddings).astype(np.float16)
    print(f"   Matrix calculated in {time.time() - start_time:.2f} seconds.")

    # 5. Save Model Artifact
    print(f"\n5. Saving optimized similarity matrix to {out_path}...")
    pickle.dump(similarity, open(out_path, 'wb'))
    
    file_size = os.path.getsize(out_path) / (1024 * 1024)
    print(f"Success! New semantic similarity model saved. Size: {file_size:.2f} MB")
    print("You can now run the Streamlit app for massively improved recommendations!")

if __name__ == "__main__":
    compute_embeddings()
