# Deployment Guide

This app is container-ready and serves with a production WSGI server
(waitress). It exposes a `/health` endpoint for uptime checks and reads
its port from the `PORT` environment variable, so it runs on any modern
platform.

Without IBM Watson credentials the app uses a built-in keyword mock, so
it works out of the box. To use real Watson NLU, set `WATSON_NLU_APIKEY`
and `WATSON_NLU_URL` as environment variables on the platform.

---

## Option A — Render (recommended, free tier)

Render reads `render.yaml` automatically as a Blueprint.

1. Push this repo to GitHub (already done).
2. Go to <https://dashboard.render.com> and sign in with GitHub.
3. Click **New +** → **Blueprint**.
4. Select the `Flask-python` repository. Render detects `render.yaml`
   and proposes a web service named `emotion-detection`.
5. Click **Apply**. Render builds the Docker image and deploys it.
6. (Optional) In the service's **Environment** tab, add real values for
   `WATSON_NLU_APIKEY` and `WATSON_NLU_URL`.

Render assigns a public URL like `https://emotion-detection.onrender.com`.
The health check hits `/health`. Note: free web services sleep after
inactivity and take a few seconds to wake on the next request.

---

## Option B — Run the prebuilt image from GHCR

Every push to `main` publishes an image to the GitHub Container Registry
via `.github/workflows/docker-publish.yml`.

```bash
docker pull ghcr.io/alphaxt/flask-python:latest
docker run -p 5000:5000 ghcr.io/alphaxt/flask-python:latest
```

Then open <http://localhost:5000>. To use Watson NLU:

```bash
docker run -p 5000:5000 \
  -e WATSON_NLU_APIKEY=your_key \
  -e WATSON_NLU_URL=your_url \
  ghcr.io/alphaxt/flask-python:latest
```

The package must be made public once (repo → Packages → package
settings) for anonymous pulls; otherwise `docker login ghcr.io` first.

---

## Option C — Fly.io

```bash
# Install flyctl, then:
fly launch --dockerfile Dockerfile --name emotion-detection
fly secrets set WATSON_NLU_APIKEY=your_key WATSON_NLU_URL=your_url
fly deploy
```

Fly injects `PORT` (default 8080) which the app honors automatically.

---

## Build and run locally with Docker

```bash
docker build -t emotion-detection .
docker run -p 5000:5000 emotion-detection
# open http://localhost:5000
```

## Verify a deployment

```bash
curl https://<your-app-url>/health
# -> {"status": "ok"}

curl "https://<your-app-url>/emotionDetector?textToAnalyze=I am so happy"
# -> {... "dominant_emotion": "joy"}
```

## Environment variables

| Variable            | Purpose                              | Default                 |
| ------------------- | ------------------------------------ | ----------------------- |
| `PORT`              | Port the server listens on           | `5000`                  |
| `HOST`              | Bind address                         | `0.0.0.0`               |
| `FLASK_DEBUG`       | Dev-server debug mode (`app.py`)     | `true`                  |
| `WATSON_NLU_APIKEY` | IBM Watson NLU API key (optional)    | mock fallback           |
| `WATSON_NLU_URL`    | IBM Watson NLU service URL (optional)| mock fallback           |
| `RATELIMIT_ENABLED` | Enable per-IP API rate limiting      | `true`                  |
| `RATELIMIT_DEFAULT` | Default limit across all routes      | `200 per hour`          |
| `RATELIMIT_API`     | Limit for `/emotionDetector`         | `30 per minute`         |
