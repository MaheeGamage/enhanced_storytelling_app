import os
from unittest.mock import patch, MagicMock
import unittest

# Mock class for testing without actual API key
class MockStoryGenerator:
    def generate_introduction(self, genre, character, mood):
        return f"This is a test introduction for a {genre} story with {character} in a {mood} mood."
    
    def generate_choices(self, story_context):
        return ["Choice 1", "Choice 2", "Choice 3"]
    
    def generate_continuation(self, story_context, choice):
        return f"This is a test continuation after choosing: {choice}"
    
    def generate_modification(self, story_context, command):
        return f"This is a test modification after command: {command}"

# Patch the StoryGenerator import in app.py
with patch('app.StoryGenerator', MockStoryGenerator):
    from app import app, process_story_command

class TestFlaskApp(unittest.TestCase):
    """Test cases for the Flask application"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_index_route(self):
        """Test the index route returns the main page"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Interactive Storytelling Assistant', response.data)
    
    def test_initialize_story(self):
        """Test the initialize_story route"""
        # Send a POST request to initialize_story
        response = self.app.post('/initialize_story', 
                                json={
                                    'genre': 'fantasy',
                                    'character': 'brave knight',
                                    'mood': 'adventurous'
                                })
        
        # Assert the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('introduction', data)
        self.assertIn('choices', data)
        self.assertEqual(len(data['choices']), 3)
    
    def test_process_story_command(self):
        """Test the process_story_command function"""
        # Test changing mood
        context = {'mood': 'adventurous'}
        process_story_command(context, "change the mood to suspenseful")
        self.assertEqual(context['mood'], "suspenseful")
        
        # Test making user the villain
        context = {}
        process_story_command(context, "make me the villain")
        self.assertEqual(context['character_role'], "villain")
        
        # Test switching setting
        context = {}
        process_story_command(context, "switch to a detective setting")
        self.assertEqual(context['setting'], "a detective")
        
        # Test starting over with new genre
        context = {'history': ['old content'], 'genre': 'fantasy'}
        process_story_command(context, "start over with a new genre sci-fi")
        self.assertEqual(context['genre'], "sci-fi")
        self.assertEqual(context['history'], [])

if __name__ == '__main__':
    unittest.main()
