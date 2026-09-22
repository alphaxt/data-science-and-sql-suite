# Emotion Detection Application

[![CI](https://github.com/alphaxt/Flask-python/actions/workflows/ci.yml/badge.svg)](https://github.com/alphaxt/Flask-python/actions/workflows/ci.yml)
[![Publish Docker image](https://github.com/alphaxt/Flask-python/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/alphaxt/Flask-python/actions/workflows/docker-publish.yml)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

**🚀 Live demo: <https://emotion-detection-uka5.onrender.com>**

An AI-based web application that detects emotions in text using IBM Watson
Natural Language Understanding (NLU). It scores five core emotions and reports
the dominant one, which makes it handy for analyzing customer feedback.

If Watson credentials are not configured, the app automatically falls back to a
built-in keyword-based mock, so it stays fully runnable for development and
testing without an API key.

> The live demo runs on Render's free tier, which sleeps after inactivity.
> The first request may take a few seconds to wake the service.

## Try it

- **Web UI:** <https://emotion-detection-uka5.onrender.com>
- **Health check:** <https://emotion-detection-uka5.onrender.com/health>
- **API:**
  ```bash
  curl "https://emotion-detection-uka5.onrender.com/emotionDetector?textToAnalyze=I%20am%20so%20happy%20today"
  # {"anger":0.0,"disgust":0.0,"fear":0.0,"joy":100.0,"sadness":0.0,"dominant_emotion":"joy"}
  ```

## Features

- **Emotion Detection**: Scores anger, disgust, fear, joy, and sadness, and
  identifies the dominant emotion.
- **Web Interface**: Clean Flask UI with a text form and results panel.
- **JSON API**: `GET /emotionDetector` endpoint for programmatic access.
- **Graceful Fallback**: Keyword-based mock when Watson credentials are absent.
- **Error Handling**: Handles invalid input, API failures, and HTTP 404/500.
- **Tests**: Unit tests for both the detector and the web routes.
- **Static Analysis**: Pylint and Flake8 configured.

## Project Structure

```
Flask-python/
├── app.py                          # Entry point (loads .env, runs the server)
├── conftest.py                     # Makes `src` importable in tests
├── setup.py                        # Package configuration (src layout)
├── requirements.txt                # Python dependencies
├── pytest.ini                      # Pytest + coverage configuration
├── .pylintrc / .flake8             # Static analysis configuration
├── .env.example                    # Sample environment configuration
├── run_tests.sh / run_tests.bat    # Test + lint helper scripts
├── src/
│   └── emotion_detection/
│       ├── __init__.py             # Package exports
│       ├── detector.py             # Core Watson NLU + mock logic
│       └── webapp.py               # Flask app factory + routes
├── tests/
│   ├── test_emotion_detection.py   # Detector unit tests
│   └── test_webapp.py              # Web route unit tests
├── templates/
│   └── index.html                  # Web interface template
└── static/
    └── style.css                   # Styling
```

## Installation

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Watson credentials** (optional):
   ```bash
   cp .env.example .env   # Windows: copy .env.example .env
   ```
   Fill in `WATSON_NLU_URL` and `WATSON_NLU_APIKEY`. If left as placeholders,
   the app uses the built-in mock.

## Usage

### Run the web application

```bash
python app.py
```

Then open `http://localhost:5000`, enter text, and click **Detect Emotion**.

The port and debug mode can be overridden via environment variables:

```bash
PORT=8080 FLASK_DEBUG=false python app.py
```

### Use the API

```bash
GET /emotionDetector?textToAnalyze=<your_text>
```

Example:
```bash
curl "http://localhost:5000/emotionDetector?textToAnalyze=I%20am%20so%20happy%20today!"
```

Response:
```json
{
  "anger": 0.0,
  "disgust": 0.0,
  "fear": 0.0,
  "joy": 100.0,
  "sadness": 0.0,
  "dominant_emotion": "joy"
}
```

## Testing

```bash
pytest
```

With an HTML coverage report:
```bash
pytest --cov=src/emotion_detection --cov-report=html
```

## Static Code Analysis

```bash
pylint src/emotion_detection app.py tests
flake8 src/emotion_detection app.py tests
```

Or run everything at once:
```bash
# Windows
run_tests.bat
# macOS/Linux
bash run_tests.sh
```

## Error Handling

The application handles:
- Invalid or empty text input (returns a clear error message)
- Missing Watson credentials (falls back to the mock implementation)
- API connection and parsing errors (returns an error result instead of crashing)
- HTTP errors (404 and 500 return JSON bodies)

## Dependencies

- **Flask** (3.0.0): Web framework
- **ibm-watson** (7.0.0): IBM Watson SDK for NLU
- **python-dotenv** (1.0.0): Environment variable loading
- **pytest** (7.4.3) / **pytest-cov** (4.1.0): Testing and coverage
- **pylint** (3.0.2) / **flake8** (6.1.0): Static analysis

## Deployment

The app is container-ready with a production WSGI server (waitress), a
`/health` endpoint, and `PORT`-aware startup. The quickest path is
**Render** via the included `render.yaml` Blueprint. Every push to `main`
also publishes a Docker image to GitHub Container Registry.

See [DEPLOY.md](DEPLOY.md) for step-by-step instructions (Render, GHCR,
Fly.io, and local Docker).

## License

Apache License 2.0
