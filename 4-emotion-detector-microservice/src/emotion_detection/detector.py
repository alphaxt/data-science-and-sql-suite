"""
Emotion Detection Module.

Provides functionality to detect emotions in text using IBM Watson
Natural Language Understanding. When Watson credentials are not
configured, a keyword-based mock implementation is used so the
application remains fully runnable for development and testing.
"""

import os

try:
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_watson.natural_language_understanding_v1 import (
        Features,
        EmotionOptions,
    )
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

    _WATSON_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    _WATSON_AVAILABLE = False


EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")

_PLACEHOLDER_APIKEY = "YOUR_API_KEY"
_PLACEHOLDER_URL_SUFFIX = "YOUR_INSTANCE_ID"


def _empty_result(error_message=None):
    """Build a result dict with all emotions set to None."""
    result = {emotion: None for emotion in EMOTIONS}
    result["dominant_emotion"] = None
    if error_message is not None:
        result["error"] = error_message
    return result


def _dominant(scores):
    """Return the key of the highest-scoring emotion."""
    return max(scores.items(), key=lambda item: item[1])[0]


def _using_placeholder_credentials(apikey, url):
    """Return True when credentials are missing or still placeholders."""
    return (
        not apikey
        or apikey == _PLACEHOLDER_APIKEY
        or not url
        or url.endswith(_PLACEHOLDER_URL_SUFFIX)
    )


def _mock_emotion_detection(text_to_analyze):
    """
    Keyword-based mock used when Watson credentials are not configured.

    Args:
        text_to_analyze (str): The text to analyze.

    Returns:
        dict: Emotion scores in the 0..1 range plus the dominant emotion.
    """
    text_lower = text_to_analyze.lower()

    keyword_map = {
        "joy": ["happy", "joy", "excited", "great", "wonderful",
                "amazing", "love", "fantastic"],
        "anger": ["angry", "mad", "furious", "annoyed", "frustrated", "hate"],
        "sadness": ["sad", "depressed", "lonely", "unhappy",
                    "miserable", "cry"],
        "fear": ["scared", "afraid", "fear", "worried", "anxious", "nervous"],
        "disgust": ["disgust", "disgusted", "revolting", "gross", "nasty"],
    }

    scores = {
        emotion: sum(1 for word in words if word in text_lower) * 0.3
        for emotion, words in keyword_map.items()
    }

    total = sum(scores.values())
    if total == 0:
        # No keyword hits: return an even, neutral distribution.
        scores = {emotion: 0.2 for emotion in keyword_map}
    else:
        scores = {emotion: value / total for emotion, value in scores.items()}

    result = {emotion: min(scores[emotion], 1.0) for emotion in EMOTIONS}
    result["dominant_emotion"] = _dominant(
        {emotion: result[emotion] for emotion in EMOTIONS}
    )
    return result


def _watson_emotion_detection(text_to_analyze, apikey, url):
    """Call IBM Watson NLU and return formatted emotion scores."""
    authenticator = IAMAuthenticator(apikey)
    service = NaturalLanguageUnderstandingV1(
        version="2021-08-01",
        authenticator=authenticator,
    )
    service.set_service_url(url)

    response = service.analyze(
        text=text_to_analyze,
        features=Features(emotion=EmotionOptions()),
    ).get_result()

    emotions = response["emotion"]["document"]["emotion"]
    result = {emotion: emotions.get(emotion, 0) for emotion in EMOTIONS}
    result["dominant_emotion"] = _dominant(
        {emotion: result[emotion] for emotion in EMOTIONS}
    )
    return result


def emotion_detector(text_to_analyze):
    """
    Detect emotions in the given text.

    Uses IBM Watson Natural Language Understanding when credentials are
    configured via the WATSON_NLU_APIKEY and WATSON_NLU_URL environment
    variables; otherwise falls back to a keyword-based mock.

    Args:
        text_to_analyze (str): The text to analyze for emotions.

    Returns:
        dict: {
            'anger': float, 'disgust': float, 'fear': float,
            'joy': float, 'sadness': float, 'dominant_emotion': str
        }
        On failure, all scores are None and an 'error' key is added.
    """
    apikey = os.getenv("WATSON_NLU_APIKEY", _PLACEHOLDER_APIKEY)
    url = os.getenv(
        "WATSON_NLU_URL",
        "https://api.us-south.natural-language-understanding.watson."
        "cloud.ibm.com/instances/" + _PLACEHOLDER_URL_SUFFIX,
    )

    if not _WATSON_AVAILABLE or _using_placeholder_credentials(apikey, url):
        return _mock_emotion_detection(text_to_analyze)

    try:
        return _watson_emotion_detection(text_to_analyze, apikey, url)
    except (KeyError, ValueError, ConnectionError) as exc:
        return _empty_result(error_message=str(exc))
    except Exception as exc:  # pylint: disable=broad-except
        # Watson SDK raises ApiException and other runtime errors we
        # cannot enumerate here; degrade gracefully rather than crash.
        return _empty_result(error_message=str(exc))


def emotion_predictor(text_to_analyze):
    """
    Predict emotions and format scores as percentages for display.

    Args:
        text_to_analyze (str): The text to analyze.

    Returns:
        dict: Emotion percentages (0..100) plus the dominant emotion,
              or an error dict for invalid input.
    """
    if not text_to_analyze or not text_to_analyze.strip():
        return _empty_result(error_message="Invalid text! Please try again.")

    result = emotion_detector(text_to_analyze)

    if "error" not in result:
        for emotion in EMOTIONS:
            if result[emotion] is not None:
                result[emotion] = round(result[emotion] * 100, 2)

    return result
