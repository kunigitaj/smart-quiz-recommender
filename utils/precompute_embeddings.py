# utils/precompute_embeddings.py

import sys
import os
import torch
import json
import numpy as np
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
import joblib  # Add this import to save/load PCA model

# Add the parent directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# Import load_json from json_utils instead of app.utils
from utils.json_utils import load_json

def precompute_embeddings():
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

    quizzes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../public/quizzes.json')
    if not os.path.exists(quizzes_path):
        raise ValueError(f"QUIZZES_JSON_PATH does not exist at {quizzes_path}")

    quizzes = load_json(quizzes_path)
    all_embeddings = []
    precomputed_data = []

    for quiz in quizzes['quizzes']:
        for question in quiz['questions']:
            title = question['title']
            correct_option_text = next(opt['text'] for opt in question['options'] if opt['id'] == question['correctOption'])
            combined_text = f"{title} {correct_option_text}"
            embedding = model.encode(combined_text, convert_to_tensor=True).cpu().numpy()
            all_embeddings.append(embedding)
            precomputed_data.append({
                'question': question,
                'embedding': embedding
            })

    all_embeddings = np.array(all_embeddings)

    # Apply PCA to reduce dimensions to, e.g., 128
    pca = PCA(n_components=128)
    reduced_embeddings = pca.fit_transform(all_embeddings)

    # Save the PCA model
    pca_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../public/pca_model.pkl')
    joblib.dump(pca, pca_model_path)

    # Quantize the reduced embeddings to 8-bit integers
    min_val = reduced_embeddings.min()
    max_val = reduced_embeddings.max()
    quantized_embeddings = np.round(255 * (reduced_embeddings - min_val) / (max_val - min_val)).astype(np.uint8)

    for i, entry in enumerate(precomputed_data):
        entry['embedding'] = quantized_embeddings[i].tolist()

    embeddings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../public/precomputed_embeddings.json')
    with open(embeddings_path, 'w') as f:
        json.dump(precomputed_data, f)

    print(f"Precomputed embeddings saved to {embeddings_path}")

if __name__ == "__main__":
    precompute_embeddings()
