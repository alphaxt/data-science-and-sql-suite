"""
Emotion Detection package.

Exposes the core emotion analysis functions.
"""

from .detector import emotion_detector, emotion_predictor

__all__ = ["emotion_detector", "emotion_predictor"]
__version__ = "1.1.0"
