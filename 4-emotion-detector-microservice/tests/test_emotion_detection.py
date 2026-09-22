"""
Unit tests for the emotion detection functionality.
"""

import unittest

from src.emotion_detection import emotion_detector, emotion_predictor


class TestEmotionDetection(unittest.TestCase):
    """Test cases for emotion detection functions."""

    def test_emotion_predictor_joy(self):
        """Joyful text should include a joy score and dominant emotion."""
        result = emotion_predictor("I am so happy today!")
        self.assertIsNotNone(result)
        self.assertIn("joy", result)
        self.assertIn("dominant_emotion", result)
        self.assertEqual(result["dominant_emotion"], "joy")

    def test_emotion_predictor_anger(self):
        """Angry text should include an anger score."""
        result = emotion_predictor("I am really mad about this!")
        self.assertIsNotNone(result)
        self.assertIn("anger", result)
        self.assertIn("dominant_emotion", result)

    def test_emotion_predictor_sadness(self):
        """Sad text should include a sadness score."""
        result = emotion_predictor("I feel so sad and lonely.")
        self.assertIsNotNone(result)
        self.assertIn("sadness", result)
        self.assertIn("dominant_emotion", result)

    def test_emotion_predictor_fear(self):
        """Fearful text should include a fear score."""
        result = emotion_predictor("I am scared of what might happen.")
        self.assertIsNotNone(result)
        self.assertIn("fear", result)
        self.assertIn("dominant_emotion", result)

    def test_emotion_predictor_empty_string(self):
        """Empty input should return an error."""
        result = emotion_predictor("")
        self.assertIsNotNone(result)
        self.assertIn("error", result)

    def test_emotion_predictor_whitespace(self):
        """Whitespace-only input should return an error."""
        result = emotion_predictor("   ")
        self.assertIn("error", result)

    def test_emotion_predictor_none(self):
        """None input should return an error."""
        result = emotion_predictor(None)
        self.assertIsNotNone(result)
        self.assertIn("error", result)

    def test_emotion_predictor_response_structure(self):
        """The response should contain all emotion keys."""
        result = emotion_predictor("This is a test statement.")
        self.assertIsInstance(result, dict)
        for key in ("anger", "disgust", "fear", "joy",
                    "sadness", "dominant_emotion"):
            self.assertIn(key, result)

    def test_emotion_predictor_percentages_in_range(self):
        """Scores should be formatted as percentages between 0 and 100."""
        result = emotion_predictor("I am so happy and excited!")
        for emotion in ("anger", "disgust", "fear", "joy", "sadness"):
            self.assertGreaterEqual(result[emotion], 0)
            self.assertLessEqual(result[emotion], 100)

    def test_emotion_detector_function_exists(self):
        """emotion_detector should be callable."""
        self.assertTrue(callable(emotion_detector))

    def test_emotion_predictor_function_exists(self):
        """emotion_predictor should be callable."""
        self.assertTrue(callable(emotion_predictor))


if __name__ == "__main__":
    unittest.main()
