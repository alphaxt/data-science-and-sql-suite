"""
Production WSGI entry point.

Exposes ``application`` for WSGI servers and, when run directly, serves
the app with waitress (a cross-platform production server).

Examples:
    waitress-serve --port=5000 wsgi:application
    python wsgi.py
"""

import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv is optional at runtime
    pass

from src.emotion_detection.webapp import create_app

application = create_app()
app = application  # convenience alias


if __name__ == "__main__":
    from waitress import serve

    port = int(os.getenv("PORT", "5000"))
    host = os.getenv("HOST", "0.0.0.0")
    print(f"Serving on http://{host}:{port} (production/waitress)")
    serve(application, host=host, port=port)
