# Interactive Storytelling Assistant

An interactive web application that generates dynamic stories in collaboration with users, powered by OpenAI's API.

## Features

- User preference collection (genre, character traits, mood)
- Dynamic story generation with compelling introductions
- Branching narrative with user choices
- Support for user interruptions and commands
- Reflective questions to deepen immersion
- Proper story ending after multiple cycles
- Responsive design for all devices

## Requirements

- Python 3.10+
- Flask
- OpenAI API key
- Modern web browser

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install flask openai python-dotenv requests
   ```
4. Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the Application

1. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```
2. Run the application:
   ```
   ./run.sh
   ```
3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## User Commands

Users can interrupt the story anytime by typing commands like:
- "Change the mood to suspenseful."
- "Make me the villain."
- "Switch to a detective setting."
- "Start over with a new genre."

## Project Structure

- `app.py`: Main Flask application
- `story_generator.py`: OpenAI API integration for story generation
- `templates/`: HTML templates
- `static/`: CSS and JavaScript files
- `tests/`: Unit tests

## Testing

Run the tests with:
```
./run_tests.sh
```

## Deployment

The application can be deployed using the Flask development server for prototyping purposes. For production deployment, consider using Gunicorn or uWSGI with Nginx.
