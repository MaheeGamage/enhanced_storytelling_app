#!/bin/bash

# Run all tests for the interactive storytelling application

# Create __init__.py file to make the tests directory a package
touch tests/__init__.py

# Run the story generator tests
echo "Running StoryGenerator tests..."
python3 -m unittest tests/test_story_generator.py

# Run the Flask app tests
echo "Running Flask application tests..."
python3 -m unittest tests/test_flask_app.py

echo "All tests completed."
