# app/__init__.py

from flask import Flask
from flask_caching import Cache
from .logger import setup_logger

cache = Cache()  # Create the cache instance

def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config.from_object('config.Config')

    # Setup logging
    setup_logger(app)

    # Initialize caching with the app
    cache.init_app(app)  # Attach the cache to the app

    # Register routes
    with app.app_context():
        from . import routes

    return app
