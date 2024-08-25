# app/embeddings.py

import os
import torch
import logging
from sentence_transformers import SentenceTransformer, util
from .utils import load_json
from .custom_tokenize import custom_tokenize
from . import cache  # Import the cache instance from __init__.py

# Load the model globally to avoid reloading it for every request
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2').to(device)

def load_quizzes():
    quizzes_path = os.getenv('QUIZZES_JSON_PATH')
    if not quizzes_path:
        raise ValueError("QUIZZES_JSON_PATH environment variable not set.")

    # Log the absolute path for debugging purposes
    logging.info(f"Loading quizzes from: {os.path.abspath(quizzes_path)}")

    try:
        return load_json(quizzes_path)
    except Exception as e:
        logging.exception(f"Error loading quizzes from {quizzes_path}")
        raise

@cache.memoize(timeout=3600)  # Use the cache instance correctly
def load_and_preprocess_quizzes():
    quizzes = load_quizzes()

    questions = []
    embeddings = []
    for quiz in quizzes['quizzes']:
        for question in quiz['questions']:
            title = question['title']
            correct_option_text = next(
                opt['text'] for opt in question['options'] if opt['id'] == question['correctOption']
            )
            combined_text = f"{title} {correct_option_text}"
            questions.append(question)

            # Directly encode the combined text into a tensor
            embedding = model.encode(combined_text, convert_to_tensor=True).to('cpu')
            embeddings.append(embedding)

    return questions, torch.stack(embeddings)

# Use the cached function to load and preprocess quizzes
questions, embeddings = load_and_preprocess_quizzes()

def recommend_questions(queries):
    recommendations = []
    for query in queries:
        query_text = f"{query['question']} {query['answer']}"

        # Directly encode the query text into a tensor
        query_embedding = model.encode(query_text, convert_to_tensor=True).to('cpu')
        
        cos_scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
        top_results = torch.topk(cos_scores, k=3).indices
        recommended_questions = [questions[idx] for idx in top_results]
        recommendations.append(recommended_questions)
    return recommendations
