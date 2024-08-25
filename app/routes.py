# app/routes.py

from flask import request, jsonify, current_app as app, abort
from .embeddings import recommend_questions
import logging
from werkzeug.exceptions import BadRequest

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        if not data or 'queries' not in data:
            abort(400, description="Invalid input: 'queries' key missing")
        
        if not isinstance(data['queries'], list):
            abort(422, description="'queries' should be a list")

        recommendations = recommend_questions(data['queries'])
        return jsonify(recommendations), 200

    except BadRequest as e:
        logging.error(f"Bad request: {str(e)}")
        return jsonify({"error": "Bad Request"}), 400
    except Exception as e:
        logging.exception("Error processing recommendation request")
        return jsonify({"error": "Internal Server Error"}), 500
