# app/__init__.py

from flask import Flask
from flask_caching import Cache
from .logger import setup_logger
import logging

cache = Cache()  # Create the cache instance

def create_app():
    logging.info("Initializing the Flask application...")

    app = Flask(__name__)
    
    # Load configurations
    app.config.from_object('config.Config')
    logging.info("Configurations loaded.")

    # Setup logging
    setup_logger(app)
    logging.info("Logger setup completed.")

    # Initialize caching with the app
    cache.init_app(app)  # Attach the cache to the app
    logging.info("Cache initialized.")

    # Register routes
    with app.app_context():
        from . import routes
        logging.info("Routes registered.")

    logging.info("Flask application initialized successfully.")
    
    return app
