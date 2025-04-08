import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Mock the OpenAI module
class MockOpenAI:
    class ChatCompletion:
        @staticmethod
        def create(*args, **kwargs):
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "This is a mock response from OpenAI API."
            return mock_response

# Add the parent directory to the path so we can import the story_generator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock the openai module
sys.modules['openai'] = MagicMock()
sys.modules['openai'].chat.completions.create = MockOpenAI.ChatCompletion.create

# Now import the StoryGenerator
from story_generator import StoryGenerator

class TestStoryGenerator(unittest.TestCase):
    """Test cases for the StoryGenerator class with mocked OpenAI API"""
    
    def setUp(self):
        """Set up the test environment"""
        # Create a patch for load_dotenv to avoid actual env loading
        self.dotenv_patcher = patch('story_generator.load_dotenv')
        self.mock_dotenv = self.dotenv_patcher.start()
        
        # Create a patch for os.getenv to return a fake API key
        self.getenv_patcher = patch('story_generator.os.getenv')
        self.mock_getenv = self.getenv_patcher.start()
        self.mock_getenv.return_value = "fake-api-key"
        
    def tearDown(self):
        """Clean up after tests"""
        self.dotenv_patcher.stop()
        self.getenv_patcher.stop()
    
    def test_generate_introduction(self):
        """Test the generate_introduction method"""
        generator = StoryGenerator()
        result = generator.generate_introduction("fantasy", "brave knight", "adventurous")
        self.assertEqual(result, "This is a mock response from OpenAI API.")
    
    def test_generate_choices(self):
        """Test the generate_choices method"""
        generator = StoryGenerator()
        story_context = {
            'genre': 'fantasy',
            'mood': 'adventurous',
            'history': [
                {'role': 'assistant', 'content': 'Story introduction.'},
                {'role': 'user', 'content': 'User choice.'}
            ]
        }
        result = generator.generate_choices(story_context)
        # Since we're mocking the JSON response, it will try to parse the mock text
        # and fall back to the default choices
        self.assertEqual(result, ["Explore further", "Turn back", "Wait and observe"])
    
    def test_generate_continuation(self):
        """Test the generate_continuation method"""
        generator = StoryGenerator()
        story_context = {
            'genre': 'fantasy',
            'mood': 'adventurous',
            'history': [
                {'role': 'assistant', 'content': 'Story introduction.'},
                {'role': 'user', 'content': 'User choice.'}
            ]
        }
        result = generator.generate_continuation(story_context, "User choice")
        self.assertEqual(result, "This is a mock response from OpenAI API.")
    
    def test_generate_modification(self):
        """Test the generate_modification method"""
        generator = StoryGenerator()
        story_context = {
            'genre': 'fantasy',
            'mood': 'adventurous',
            'history': [
                {'role': 'assistant', 'content': 'Story introduction.'},
                {'role': 'user', 'content': 'User choice.'},
                {'role': 'assistant', 'content': 'Story continuation.'},
                {'role': 'user', 'content': 'COMMAND: Change the mood to suspenseful.'}
            ]
        }
        result = generator.generate_modification(story_context, "Change the mood to suspenseful")
        self.assertEqual(result, "This is a mock response from OpenAI API.")

if __name__ == '__main__':
    unittest.main()
