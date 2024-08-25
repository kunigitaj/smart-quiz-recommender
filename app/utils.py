# app/utils.py

import json
import os
import logging

def load_json(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def handle_error(e, message="An error occurred"):
    logging.error(message)
    logging.exception(e)
    return {"error": message}, 500
