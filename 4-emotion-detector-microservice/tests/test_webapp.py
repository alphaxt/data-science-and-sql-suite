"""
Unit tests for the Flask web application.
"""

import os
import unittest
from unittest import mock

from src.emotion_detection.webapp import create_app


class TestWebApp(unittest.TestCase):
    """Test cases for the Flask routes (rate limiting disabled)."""

    def setUp(self):
        """Create a test client with rate limiting disabled."""
        # Disable limiting so repeated calls in the suite stay deterministic.
        self.env = mock.patch.dict(
            os.environ, {"RATELIMIT_ENABLED": "false"}, clear=False
        )
        self.env.start()
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def tearDown(self):
        """Stop the env patch."""
        self.env.stop()

    def test_index_get(self):
        """GET / should render the page successfully."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_post_valid(self):
        """POST / with text should render results."""
        response = self.client.post("/", data={"text": "I am so happy!"})
        self.assertEqual(response.status_code, 200)

    def test_index_post_empty(self):
        """POST / with empty text should still render (with error)."""
        response = self.client.post("/", data={"text": ""})
        self.assertEqual(response.status_code, 200)

    def test_api_valid(self):
        """API should return 200 and emotion data for valid input."""
        response = self.client.get(
            "/emotionDetector?textToAnalyze=I am so happy!"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("dominant_emotion", response.get_json())

    def test_api_missing_text(self):
        """API should return 400 when text is missing."""
        response = self.client.get("/emotionDetector")
        self.assertEqual(response.status_code, 400)

    def test_api_empty_text(self):
        """API should return 400 for empty text."""
        response = self.client.get("/emotionDetector?textToAnalyze=")
        self.assertEqual(response.status_code, 400)

    def test_health(self):
        """Health endpoint should return 200 with status ok."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_not_found(self):
        """Unknown routes should return a JSON 404."""
        response = self.client.get("/does-not-exist")
        self.assertEqual(response.status_code, 404)


class TestRateLimiting(unittest.TestCase):
    """Verify per-IP rate limiting on the API endpoint."""

    def setUp(self):
        """Create an app with a very small API limit enabled."""
        self.env = mock.patch.dict(
            os.environ,
            {
                "RATELIMIT_ENABLED": "true",
                "RATELIMIT_API": "3 per minute",
                "RATELIMIT_DEFAULT": "1000 per hour",
            },
            clear=False,
        )
        self.env.start()
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def tearDown(self):
        """Stop the env patch."""
        self.env.stop()

    def test_api_blocks_after_limit(self):
        """The 4th request within the window should return 429."""
        url = "/emotionDetector?textToAnalyze=I am happy"
        statuses = [self.client.get(url).status_code for _ in range(4)]
        self.assertEqual(statuses[:3], [200, 200, 200])
        self.assertEqual(statuses[3], 429)

    def test_health_is_exempt(self):
        """Health check should never be rate limited."""
        statuses = [self.client.get("/health").status_code for _ in range(6)]
        self.assertTrue(all(s == 200 for s in statuses))


if __name__ == "__main__":
    unittest.main()
