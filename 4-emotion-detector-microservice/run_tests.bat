@echo off
REM Run tests and static code analysis on Windows.

echo Running unit tests...
pytest -v

echo.
echo Running Pylint...
pylint src/emotion_detection app.py tests

echo.
echo Running Flake8...
flake8 src/emotion_detection app.py tests

echo.
echo All checks completed!
