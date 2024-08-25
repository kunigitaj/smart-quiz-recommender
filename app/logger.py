# app/logger.py

import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(app):
    # Ensure the logs directory exists
    logs_dir = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Stream handler (console)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    # File handler (log to a file)
    file_handler = RotatingFileHandler(os.path.join(logs_dir, 'app.log'), maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Adding handlers
    app.logger.addHandler(stream_handler)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    logging.info("Logger initialized")
