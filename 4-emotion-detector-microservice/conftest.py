"""
Pytest configuration.

Ensures the project root is importable so ``from src.emotion_detection
import ...`` works regardless of the directory pytest is invoked from.
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
