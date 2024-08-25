# config.py

import os

class Config:
    DEBUG = os.getenv('FLASK_DEBUG', False)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    QUIZZES_JSON_PATH = os.getenv('QUIZZES_JSON_PATH', os.path.join(BASE_DIR, 'data', 'quizzes.json'))
    MODEL_NAME = os.getenv('MODEL_NAME', 'sentence-transformers/all-mpnet-base-v2')
