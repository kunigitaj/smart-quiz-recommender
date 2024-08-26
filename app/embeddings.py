# app/embeddings.py

import os
import torch
import numpy as np
import json
import logging
from sentence_transformers import SentenceTransformer, util
from sklearn.decomposition import PCA
import joblib
from io import BytesIO
from .firebase_config import get_storage_bucket
from . import cache

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2').to(device)

def download_file_from_firebase(filename):
    bucket = get_storage_bucket()
    blob = bucket.blob(filename)
    file_data = blob.download_as_bytes()
    return file_data

def dequantize_embeddings(quantized_embeddings, min_val, max_val):
    return quantized_embeddings * (max_val - min_val) / 255.0 + min_val

def load_precomputed_data():
    # Download precomputed embeddings from Firebase
    precomputed_data_bytes = download_file_from_firebase('precomputed_embeddings.json')
    precomputed_data = json.loads(precomputed_data_bytes.decode('utf-8'))

    questions = [entry['question'] for entry in precomputed_data]
    quantized_embeddings = np.array([entry['embedding'] for entry in precomputed_data], dtype=np.uint8)
    
    min_val = 0  # Replace with actual value
    max_val = 1  # Replace with actual value
    
    embeddings = torch.tensor(dequantize_embeddings(quantized_embeddings, min_val, max_val), dtype=torch.float32)
    return questions, embeddings

@cache.memoize(timeout=3600)
def get_precomputed_data():
    return load_precomputed_data()

# Load PCA model from Firebase
pca_model_bytes = download_file_from_firebase('pca_model.pkl')
pca = joblib.load(BytesIO(pca_model_bytes))

questions, embeddings = get_precomputed_data()

def recommend_questions(queries):
    recommendations = []
    for query in queries:
        query_text = f"{query['question']} {query['answer']}"

        query_embedding = model.encode(query_text, convert_to_tensor=True).cpu().numpy()
        query_embedding = query_embedding.reshape(1, -1)

        query_embedding_reduced = pca.transform(query_embedding)
        query_embedding_reduced = torch.tensor(query_embedding_reduced, dtype=torch.float32).to(device)

        cos_scores = util.pytorch_cos_sim(query_embedding_reduced, embeddings)[0]
        top_results = torch.topk(cos_scores, k=3).indices
        recommended_questions = [questions[idx] for idx in top_results]
        recommendations.append(recommended_questions)
    return recommendations
