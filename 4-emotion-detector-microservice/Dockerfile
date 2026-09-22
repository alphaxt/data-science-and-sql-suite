# syntax=docker/dockerfile:1

FROM python:3.12-slim

# Keep Python lean and unbuffered for container logs.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000

WORKDIR /app

# Install dependencies first to leverage Docker layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source.
COPY . .

# Run as a non-root user for safety.
RUN useradd --create-home appuser
USER appuser

EXPOSE 5000

# Serve with the production WSGI server. wsgi.py reads the PORT env var,
# which hosting platforms (Render, Fly, Railway) inject at runtime.
CMD ["python", "wsgi.py"]
