from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
import json
from story_generator import StoryGenerator

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Initialize story generator
story_generator = StoryGenerator()

@app.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')

@app.route('/test')
def test_page():
    """Render the main page of the application."""
    return render_template('test.html')

@app.route('/initialize_story', methods=['POST'])
def initialize_story():
    """Initialize a new story based on user preferences."""
    data = request.json
    genre = data.get('genre', '')
    character = data.get('character', '')
    mood = data.get('mood', '')
    
    # Store user preferences in session
    session['story_context'] = {
        'genre': genre,
        'character': character,
        'mood': mood,
        'history': []  # To store conversation history
    }
    
    # Generate story introduction using OpenAI
    introduction, choices, image_url = story_generator.generate_introduction(genre, character, mood)
    
    # Update story context with the introduction
    session['story_context']['history'].append({
        'role': 'assistant',
        'content': introduction
    })
    
    return jsonify({
        'introduction': introduction,
        'choices': choices,
        'image_url': image_url
    })

@app.route('/continue_story', methods=['POST'])
def continue_story():
    """Continue the story based on user's choice."""
    data = request.json
    choice = data.get('choice', '')
    
    # Add user's choice to history
    session['story_context']['history'].append({
        'role': 'user',
        'content': choice
    })
    
    # Generate story continuation
    continuation, choices, image_url = story_generator.generate_continuation(session['story_context'], choice)
    
    # Add continuation to history
    session['story_context']['history'].append({
        'role': 'assistant',
        'content': continuation
    })
    
    return jsonify({
        'continuation': continuation,
        'choices': choices,
        'image_url': image_url
    })

@app.route('/modify_story', methods=['POST'])
def modify_story():
    """Modify the story based on user's command."""
    data = request.json
    command = data.get('command', '')
    
    # Add user's command to history
    session['story_context']['history'].append({
        'role': 'user',
        'content': f"COMMAND: {command}"
    })
    
    # Process the command and modify story context
    process_story_command(session['story_context'], command)
    
    # Generate story continuation based on the command
    continuation, choices, image_url = story_generator.generate_modification(session['story_context'], command)
    
    # Add continuation to history
    session['story_context']['history'].append({
        'role': 'assistant',
        'content': continuation
    })
    
    return jsonify({
        'continuation': continuation,
        'choices': choices,
        'image_url': image_url
    })

def process_story_command(context, command):
    """Process a user command to modify the story."""
    command = command.lower()
    
    # Handle different types of commands
    if "change the mood to" in command:
        new_mood = command.replace("change the mood to", "").strip()
        context['mood'] = new_mood
    elif "make me the villain" in command:
        context['character_role'] = "villain"
    elif "switch to" in command and "setting" in command:
        new_setting = command.replace("switch to", "").replace("setting", "").strip()
        context['setting'] = new_setting
    elif "start over with" in command and "genre" in command:
        new_genre = command.replace("start over with", "").replace("genre", "").strip()
        context['genre'] = new_genre
        context['history'] = []  # Clear history for a fresh start

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
