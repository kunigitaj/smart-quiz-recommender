# app/__init__.py

from flask import Flask
from .logger import setup_logger

def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config.from_object('config.Config')

    # Setup logging
    setup_logger(app)

    # Register routes
    with app.app_context():
        from . import routes

    return app
