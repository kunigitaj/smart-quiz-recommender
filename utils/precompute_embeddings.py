# utils/precompute_embeddings.py

import sys
import os
import torch
import json
from sentence_transformers import SentenceTransformer

# Add the parent directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import load_json from json_utils instead of app.utils
from utils.json_utils import load_json

def precompute_embeddings():
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

    # Hardcoded path to the quizzes.json file in the public folder
    quizzes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../public/quizzes.json')

    if not os.path.exists(quizzes_path):
        raise ValueError(f"QUIZZES_JSON_PATH does not exist at {quizzes_path}")

    quizzes = load_json(quizzes_path)

    precomputed_data = []
    for quiz in quizzes['quizzes']:
        for question in quiz['questions']:
            title = question['title']
            correct_option_text = next(
                opt['text'] for opt in question['options'] if opt['id'] == question['correctOption']
            )
            combined_text = f"{title} {correct_option_text}"
            embedding = model.encode(combined_text, convert_to_tensor=True).tolist()
            precomputed_data.append({
                'question': question,
                'embedding': embedding
            })

    # Hardcoded path to save the precomputed_embeddings.json file one level up
    embeddings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../public/precomputed_embeddings.json')

    # Save precomputed data to a file
    with open(embeddings_path, 'w') as f:
        json.dump(precomputed_data, f)

    print(f"Precomputed embeddings saved to {embeddings_path}")

if __name__ == "__main__":
    precompute_embeddings()
