"""Package configuration for the Emotion Detection application."""

from setuptools import setup, find_packages

setup(
    name="emotion-detection",
    version="1.1.0",
    description="AI-based emotion detection web application using Watson NLP",
    author="Emotion Detection Project",
    author_email="dev@example.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "flask==3.0.0",
        "ibm-watson==7.0.0",
        "python-dotenv==1.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "emotion-detection=app:app.run",
        ],
    },
)
