"""
Flask web application for Emotion Detection.

Serves an HTML form at ``/`` and a JSON API at ``/emotionDetector``.
Use :func:`create_app` to build the application instance.
"""

import os

from flask import Flask, render_template, request

try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    _LIMITER_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    _LIMITER_AVAILABLE = False

from .detector import emotion_predictor

# Project root is two levels up from this file (src/emotion_detection/).
_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)


def create_app():
    """Create and configure the Flask application."""
    app = Flask(
        "Emotion Detection",
        template_folder=os.path.join(_PROJECT_ROOT, "templates"),
        static_folder=os.path.join(_PROJECT_ROOT, "static"),
    )

    # Per-IP rate limiting. Enabled by default; opt out with
    # RATELIMIT_ENABLED=false (e.g. in tests). Limits are configurable
    # via RATELIMIT_DEFAULT and RATELIMIT_API.
    rate_enabled = os.getenv("RATELIMIT_ENABLED", "true").lower() == "true"
    default_limit = os.getenv("RATELIMIT_DEFAULT", "200 per hour")
    api_limit = os.getenv("RATELIMIT_API", "30 per minute")

    limiter = None
    if _LIMITER_AVAILABLE and rate_enabled:
        limiter = Limiter(
            key_func=get_remote_address,
            app=app,
            default_limits=[default_limit],
            storage_uri="memory://",
        )

    @app.route("/", methods=["GET", "POST"])
    def index():
        """Render the main page and process form submissions."""
        if request.method == "POST":
            text_to_analyze = request.form.get("text", "")

            if not text_to_analyze or not text_to_analyze.strip():
                return render_template(
                    "index.html",
                    result={"error": "Invalid text! Please try again."},
                )

            result = emotion_predictor(text_to_analyze)
            return render_template("index.html", result=result)

        return render_template("index.html")

    @app.route("/health")
    def health():
        """Lightweight health check for uptime monitoring and platforms."""
        return {"status": "ok"}, 200

    def emotion_detector_route():
        """JSON API endpoint for emotion detection."""
        text_to_analyze = request.args.get("textToAnalyze")

        if not text_to_analyze or not text_to_analyze.strip():
            return {"error": "Invalid text! Please try again."}, 400

        response = emotion_predictor(text_to_analyze)

        if "error" in response:
            return response, 400

        return response, 200

    # Register the route with a stricter per-IP limit on the API.
    if limiter is not None:
        emotion_detector_route = limiter.limit(api_limit)(  # noqa: F811
            emotion_detector_route
        )
        limiter.exempt(health)
    app.add_url_rule("/emotionDetector", "emotion_detector_route",
                     emotion_detector_route)

    @app.errorhandler(429)
    def ratelimit_exceeded(error):
        """Handle rate-limit errors with a JSON body."""
        return {
            "error": "Too many requests. Please slow down and try again.",
            "detail": str(error.description),
        }, 429

    @app.errorhandler(404)
    def not_found(_error):
        """Handle 404 errors with a JSON body."""
        return {"error": "Page not found"}, 404

    @app.errorhandler(500)
    def internal_error(_error):
        """Handle 500 errors with a JSON body."""
        return {"error": "Internal server error"}, 500

    return app
