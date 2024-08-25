# run.py

from app import create_app
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Setup logging format
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

app = create_app()

if __name__ == '__main__':
    logging.info("Starting the Flask application...")

    # For local development
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    logging.info(f"Debug mode is {'on' if debug_mode else 'off'}")

    port = int(os.environ.get('PORT', 5001))
    logging.info(f"Running on http://0.0.0.0:{port}")

    app.run(host='0.0.0.0', port=port, debug=debug_mode)
