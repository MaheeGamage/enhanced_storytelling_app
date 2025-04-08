#!/bin/bash

# Test script for the interactive storytelling application

# Check if .env file exists and has a valid API key
if [ ! -f .env ]; then
    echo "ERROR: .env file not found. Creating a template .env file."
    echo "# OpenAI API Key" > .env
    echo "# Replace with your actual API key" >> .env
    echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
    echo "Please edit the .env file with your actual OpenAI API key before running the application."
    exit 1
fi

# Check if API key is set to the default value
if grep -q "your_openai_api_key_here" .env; then
    echo "WARNING: You need to set your actual OpenAI API key in the .env file."
    echo "The application will not work properly without a valid API key."
fi

# Run the test script to verify OpenAI API connection
echo "Testing OpenAI API connection..."
python3 test_openai.py

# If the test fails, exit
if [ $? -ne 0 ]; then
    echo "OpenAI API test failed. Please check your API key and internet connection."
    exit 1
fi

# Start the Flask application
echo "Starting the Flask application..."
echo "The application will be available at http://localhost:5000"
echo "Press Ctrl+C to stop the server"
python3 app.py
