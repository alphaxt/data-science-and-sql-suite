"""
Application entry point for the Emotion Detection web app.

Loads environment variables (from a local ``.env`` if present), builds
the Flask app via the application factory, and runs the development
server.

Run with:
    python app.py
"""

import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv is optional at runtime
    pass

from src.emotion_detection.webapp import create_app

app = create_app()


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=debug)
