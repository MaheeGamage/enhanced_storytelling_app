import os
from dotenv import load_dotenv
import openai

# Test script to verify OpenAI API integration

# Load environment variables
load_dotenv()

# Configure OpenAI API
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your_openai_api_key_here":
    print("ERROR: Please set your OpenAI API key in the .env file")
    exit(1)

openai.api_key = api_key

def test_openai_connection():
    """Test the connection to OpenAI API"""
    try:
        print("Testing OpenAI API connection...")
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a storyteller."},
                {"role": "user", "content": "Create a one-sentence story introduction."}
            ],
            max_tokens=50
        )
        print("Connection successful!")
        print("Sample response:", response.choices[0].message.content)
        return True
    except Exception as e:
        print(f"Error connecting to OpenAI API: {e}")
        return False

if __name__ == "__main__":
    test_openai_connection()
