# app/wsgi.py

from app import create_app

app = create_app()

if __name__ != "__main__":
    # This ensures the app runs properly when invoked by Vercel's WSGI server
    application = app
