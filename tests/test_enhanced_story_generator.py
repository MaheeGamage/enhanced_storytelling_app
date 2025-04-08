import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import the story_generator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create a test class for the enhanced StoryGenerator
class TestEnhancedStoryGenerator(unittest.TestCase):
    """Test cases for the enhanced StoryGenerator class with mocked OpenAI API"""
    
    def setUp(self):
        """Set up the test environment"""
        # Create patches for the required modules and classes
        self.dotenv_patcher = patch('story_generator.load_dotenv')
        self.getenv_patcher = patch('story_generator.os.getenv', return_value="fake-api-key")
        self.openai_patcher = patch('story_generator.openai')
        
        # Start the patches
        self.mock_dotenv = self.dotenv_patcher.start()
        self.mock_getenv = self.getenv_patcher.start()
        self.mock_openai = self.openai_patcher.start()
        
        # Configure the mock OpenAI
        self.mock_openai.api_key = "fake-api-key"
        
        # Mock the chat completions create method
        mock_chat_response = MagicMock()
        mock_chat_response.choices = [MagicMock()]
        mock_chat_response.choices[0].message.content = "This is a mock story response.\n\nCHOICES: [\"Option 1\", \"Option 2\", \"Option 3\"]"
        self.mock_openai.chat.completions.create.return_value = mock_chat_response
        
        # Mock the images generate method
        mock_image_response = MagicMock()
        mock_image_response.data = [MagicMock()]
        mock_image_response.data[0].url = "https://example.com/mock-image.jpg"
        self.mock_openai.images.generate.return_value = mock_image_response
        
        # Import the StoryGenerator class after patching
        from story_generator import StoryGenerator
        self.StoryGenerator = StoryGenerator
    
    def tearDown(self):
        """Clean up after tests"""
        self.dotenv_patcher.stop()
        self.getenv_patcher.stop()
        self.openai_patcher.stop()
    
    def test_generate_introduction(self):
        """Test the enhanced generate_introduction method with image generation"""
        generator = self.StoryGenerator()
        introduction, choices, image_url = generator.generate_introduction("fantasy", "brave knight", "adventurous")
        
        # Check the introduction
        self.assertEqual(introduction, "This is a mock story response.")
        
        # Check the choices
        self.assertEqual(choices, ["Option 1", "Option 2", "Option 3"])
        
        # Check the image URL
        self.assertEqual(image_url, "https://example.com/mock-image.jpg")
    
    def test_generate_continuation(self):
        """Test the enhanced generate_continuation method with image generation"""
        generator = self.StoryGenerator()
        story_context = {
            'genre': 'fantasy',
            'mood': 'adventurous',
            'history': [
                {'role': 'assistant', 'content': 'Story introduction.'},
                {'role': 'user', 'content': 'User choice.'}
            ]
        }
        
        continuation, choices, image_url = generator.generate_continuation(story_context, "User choice")
        
        # Check the continuation
        self.assertEqual(continuation, "This is a mock story response.")
        
        # Check the choices
        self.assertEqual(choices, ["Option 1", "Option 2", "Option 3"])
        
        # Check the image URL
        self.assertEqual(image_url, "https://example.com/mock-image.jpg")
    
    def test_generate_modification(self):
        """Test the enhanced generate_modification method with image generation"""
        generator = self.StoryGenerator()
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
        
        modification, choices, image_url = generator.generate_modification(story_context, "Change the mood to suspenseful")
        
        # Check the modification
        self.assertEqual(modification, "This is a mock story response.")
        
        # Check the choices
        self.assertEqual(choices, ["Option 1", "Option 2", "Option 3"])
        
        # Check the image URL
        self.assertEqual(image_url, "https://example.com/mock-image.jpg")
    
    def test_extract_choices(self):
        """Test the _extract_choices method"""
        generator = self.StoryGenerator()
        
        # Test with valid CHOICES section
        content = "Story text.\n\nCHOICES: [\"Option 1\", \"Option 2\", \"Option 3\"]"
        choices = generator._extract_choices(content)
        self.assertEqual(choices, ["Option 1", "Option 2", "Option 3"])
        
        # Test with no CHOICES section
        content = "Story text without choices."
        choices = generator._extract_choices(content)
        self.assertEqual(choices, ["Continue the adventure", "Take a different path", "Rest and reconsider"])
    
    def test_remove_choices_section(self):
        """Test the _remove_choices_section method"""
        generator = self.StoryGenerator()
        
        # Test with CHOICES section
        content = "Story text.\n\nCHOICES: [\"Option 1\", \"Option 2\", \"Option 3\"]"
        cleaned_content = generator._remove_choices_section(content)
        self.assertEqual(cleaned_content, "Story text.")
        
        # Test without CHOICES section
        content = "Story text without choices."
        cleaned_content = generator._remove_choices_section(content)
        self.assertEqual(cleaned_content, "Story text without choices.")

if __name__ == '__main__':
    unittest.main()
