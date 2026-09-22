"""
Unit tests for the live IBM Watson NLU code path.

These tests patch the Watson SDK and environment variables so the
"real" branch of ``emotion_detector`` runs without any network calls or
credentials, closing the coverage gap left by the mock fallback.
"""

import unittest
from unittest import mock

from src.emotion_detection import detector


def _valid_env():
    """Environment with non-placeholder Watson credentials."""
    return {
        "WATSON_NLU_APIKEY": "real-key-123",
        "WATSON_NLU_URL": "https://example.com/instances/abc-123",
    }


class TestWatsonBranch(unittest.TestCase):
    """Exercise the Watson-backed detection path via mocks."""

    def test_watson_success_returns_scores(self):
        """A successful Watson call is formatted into emotion scores."""
        fake_service = mock.MagicMock()
        fake_service.analyze.return_value.get_result.return_value = {
            "emotion": {
                "document": {
                    "emotion": {
                        "anger": 0.05,
                        "disgust": 0.02,
                        "fear": 0.03,
                        "joy": 0.85,
                        "sadness": 0.05,
                    }
                }
            }
        }

        with mock.patch.dict(detector.os.environ, _valid_env(), clear=False), \
                mock.patch.object(detector, "_WATSON_AVAILABLE", True), \
                mock.patch.object(detector, "IAMAuthenticator", create=True), \
                mock.patch.object(
                    detector, "NaturalLanguageUnderstandingV1",
                    create=True, return_value=fake_service), \
                mock.patch.object(detector, "Features", create=True), \
                mock.patch.object(detector, "EmotionOptions", create=True):
            result = detector.emotion_detector("I love this!")

        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertAlmostEqual(result["joy"], 0.85)
        self.assertNotIn("error", result)

    def test_watson_failure_returns_error(self):
        """An exception from Watson yields an error result, not a crash."""
        with mock.patch.dict(detector.os.environ, _valid_env(), clear=False), \
                mock.patch.object(detector, "_WATSON_AVAILABLE", True), \
                mock.patch.object(detector, "IAMAuthenticator", create=True), \
                mock.patch.object(
                    detector, "NaturalLanguageUnderstandingV1",
                    create=True,
                    side_effect=RuntimeError("boom")), \
                mock.patch.object(detector, "Features", create=True), \
                mock.patch.object(detector, "EmotionOptions", create=True):
            result = detector.emotion_detector("anything")

        self.assertIn("error", result)
        self.assertEqual(result["error"], "boom")
        self.assertIsNone(result["joy"])
        self.assertIsNone(result["dominant_emotion"])

    def test_placeholder_credentials_use_mock(self):
        """Placeholder credentials should route to the mock path."""
        env = {
            "WATSON_NLU_APIKEY": "YOUR_API_KEY",
            "WATSON_NLU_URL": "https://x/instances/YOUR_INSTANCE_ID",
        }
        with mock.patch.dict(detector.os.environ, env, clear=False):
            result = detector.emotion_detector("I am happy")
        self.assertNotIn("error", result)
        self.assertEqual(result["dominant_emotion"], "joy")

    def test_watson_unavailable_uses_mock(self):
        """When the SDK is not importable, the mock path is used."""
        with mock.patch.dict(detector.os.environ, _valid_env(), clear=False), \
                mock.patch.object(detector, "_WATSON_AVAILABLE", False):
            result = detector.emotion_detector("I am scared")
        self.assertNotIn("error", result)
        self.assertEqual(result["dominant_emotion"], "fear")


if __name__ == "__main__":
    unittest.main()
