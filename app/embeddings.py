# app/embeddings.py

import os
import torch
import json
import logging
from sentence_transformers import SentenceTransformer, util
from . import cache  # Import the cache instance from __init__.py

# Load the model globally to avoid reloading it for every request
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2').to(device)

# Load the precomputed embeddings
def load_precomputed_data():
    with open('public/precomputed_embeddings.json', 'r') as f:  # Use the correct path to the file
        precomputed_data = json.load(f)

    questions = [entry['question'] for entry in precomputed_data]
    embeddings = torch.tensor([entry['embedding'] for entry in precomputed_data])
    return questions, embeddings

@cache.memoize(timeout=3600)  # Cache for 1 hour
def get_precomputed_data():
    return load_precomputed_data()

questions, embeddings = get_precomputed_data()

def recommend_questions(queries):
    recommendations = []
    for query in queries:
        query_text = f"{query['question']} {query['answer']}"

        # Directly encode the query text into a tensor
        query_embedding = model.encode(query_text, convert_to_tensor=True)
        
        cos_scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
        top_results = torch.topk(cos_scores, k=3).indices
        recommended_questions = [questions[idx] for idx in top_results]
        recommendations.append(recommended_questions)
    return recommendations
