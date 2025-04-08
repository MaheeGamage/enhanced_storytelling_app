import os
from dotenv import load_dotenv
import openai
import json
import requests
from io import BytesIO
import base64

class StoryGenerator:
    """Enhanced class to handle all OpenAI API interactions for story generation"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Configure OpenAI API
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            raise ValueError("Please set your OpenAI API key in the .env file")
        
        openai.api_key = api_key
        self.model = "gpt-3.5-turbo"
        self.image_size = "512x512"  # Default image size
    
    def generate_introduction(self, genre, character, mood):
        """Generate a story introduction based on user preferences with embedded choices and image"""
        try:
            prompt = f"""
            Create a compelling introduction (2-3 paragraphs) for an interactive story with the following parameters:
            - Genre/Theme: {genre}
            - Main Character: {character}
            - Mood/Feeling: {mood}
            
            The introduction should set the scene and introduce the characters. Make it engaging and immersive.
            
            After the introduction, provide 3 possible choices for what could happen next in the story.
            Format the choices as a JSON array at the end of your response, like this:
            CHOICES: ["First option", "Second option", "Third option"]
            
            Make sure the choices are diverse and would lead to different narrative paths.
            """
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert storyteller creating an interactive narrative."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Extract choices from the content
            choices = self._extract_choices(content)
            
            # Remove the CHOICES section from the content
            introduction = self._remove_choices_section(content)
            
            # Generate an image for the introduction
            image_prompt = self._generate_image_prompt(genre, character, mood, introduction)
            image_url = self._generate_image(image_prompt)
            
            return introduction, choices, image_url
        except Exception as e:
            print(f"Error generating story introduction: {e}")
            return f"Error generating story introduction: {str(e)}", ["Continue the story", "Try a different approach", "Start over"], None
    
    def generate_choices(self, story_context):
        """Generate 2-3 choices for the next part of the story - this is now handled within the continuation"""
        try:
            history_text = "\n".join([item['content'] for item in story_context['history']])
            
            prompt = f"""
            Based on the following story so far:
            
            {history_text}
            
            Generate 3 interesting choices for what could happen next in the story. 
            Format them as a JSON array of strings, each representing a possible choice.
            Example: ["Investigate the strange noise", "Return to the village", "Follow the glowing trail"]
            
            Make sure the choices are diverse and would lead to different narrative paths.
            """
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert storyteller creating interactive narrative choices."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8
            )
            
            # Parse the response to extract the choices
            choices_text = response.choices[0].message.content
            try:
                # Try to extract JSON array from the response
                choices = json.loads(choices_text)
                if not isinstance(choices, list) or len(choices) == 0:
                    choices = ["Explore further", "Turn back", "Wait and observe"]
            except:
                # Fallback if JSON parsing fails
                choices = ["Explore further", "Turn back", "Wait and observe"]
            
            return choices
        except Exception as e:
            print(f"Error generating story choices: {e}")
            return ["Continue the adventure", "Take a different path", "Rest and reconsider"]
    
    def generate_continuation(self, story_context, choice):
        """Generate the next part of the story based on the user's choice with embedded choices and image"""
        try:
            history_text = "\n".join([item['content'] for item in story_context['history']])
            
            prompt = f"""
            Based on the following story so far:
            
            {history_text}
            
            The user has chosen: "{choice}"
            
            Continue the story for 2-3 paragraphs based on this choice. Make it engaging and immersive, 
            maintaining the established {story_context['genre']} genre and {story_context['mood']} mood.
            
            Include rich descriptions, dramatic tension, and emotional involvement.
            
            After your continuation, provide 3 possible choices for what could happen next in the story.
            Format the choices as a JSON array at the end of your response, like this:
            CHOICES: ["First option", "Second option", "Third option"]
            
            Make sure the choices are diverse and would lead to different narrative paths.
            """
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert storyteller creating an interactive narrative."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Extract choices from the content
            choices = self._extract_choices(content)
            
            # Remove the CHOICES section from the content
            continuation = self._remove_choices_section(content)
            
            # Generate an image for the continuation
            image_prompt = self._generate_image_prompt(
                story_context['genre'], 
                story_context.get('character', 'protagonist'), 
                story_context['mood'], 
                continuation
            )
            image_url = self._generate_image(image_prompt)
            
            return continuation, choices, image_url
        except Exception as e:
            print(f"Error generating story continuation: {e}")
            return f"Error generating story continuation: {str(e)}", ["Continue the adventure", "Take a different path", "Rest and reconsider"], None
    
    def generate_modification(self, story_context, command):
        """Generate a modified story continuation based on the user's command with embedded choices and image"""
        try:
            history_text = "\n".join([item['content'] for item in story_context['history'][:-1]])  # Exclude the command
            
            prompt = f"""
            Based on the following story so far:
            
            {history_text}
            
            The user has issued this command: "{command}"
            
            Modify the story to incorporate this change. Write 2-3 paragraphs that continue the narrative 
            while adapting to the requested modification. Maintain character continuity and coherence.
            
            If the command is to change the mood, adjust the tone accordingly.
            If the command is to change a character role, reframe the narrative from that perspective.
            If the command is to change the setting, transition the story to that new environment.
            If the command is to start over with a new genre, begin a new story in that genre.
            
            After your continuation, provide 3 possible choices for what could happen next in the story.
            Format the choices as a JSON array at the end of your response, like this:
            CHOICES: ["First option", "Second option", "Third option"]
            
            Make sure the choices are diverse and would lead to different narrative paths.
            """
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert storyteller creating an interactive narrative."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.8
            )
            
            content = response.choices[0].message.content
            
            # Extract choices from the content
            choices = self._extract_choices(content)
            
            # Remove the CHOICES section from the content
            modification = self._remove_choices_section(content)
            
            # Update mood if it was changed in the command
            mood = story_context['mood']
            if "change the mood to" in command.lower():
                mood = command.lower().replace("change the mood to", "").strip()
            
            # Generate an image for the modification
            image_prompt = self._generate_image_prompt(
                story_context['genre'], 
                story_context.get('character', 'protagonist'), 
                mood, 
                modification
            )
            image_url = self._generate_image(image_prompt)
            
            return modification, choices, image_url
        except Exception as e:
            print(f"Error generating story modification: {e}")
            return f"Error generating story modification: {str(e)}", ["Continue the adventure", "Take a different path", "Rest and reconsider"], None
    
    def _extract_choices(self, content):
        """Extract choices from the content"""
        try:
            # Check if there's a CHOICES section
            if "CHOICES:" in content:
                choices_text = content.split("CHOICES:")[1].strip()
                # Try to parse as JSON
                try:
                    choices = json.loads(choices_text)
                    if isinstance(choices, list) and len(choices) > 0:
                        return choices
                except:
                    # If JSON parsing fails, try to extract from brackets
                    if choices_text.startswith("[") and "]" in choices_text:
                        choices_text = choices_text[choices_text.find("["):choices_text.find("]")+1]
                        try:
                            choices = json.loads(choices_text)
                            if isinstance(choices, list) and len(choices) > 0:
                                return choices
                        except:
                            pass
            
            # If we couldn't extract choices, generate them
            return ["Continue the adventure", "Take a different path", "Rest and reconsider"]
        except Exception as e:
            print(f"Error extracting choices: {e}")
            return ["Continue the adventure", "Take a different path", "Rest and reconsider"]
    
    def _remove_choices_section(self, content):
        """Remove the CHOICES section from the content"""
        if "CHOICES:" in content:
            return content.split("CHOICES:")[0].strip()
        return content
    
    def _generate_image_prompt(self, genre, character, mood, story_text):
        """Generate a prompt for image generation based on the story context directly"""
        try:
            # Extract the first 500 characters to work with
            text = story_text[:500].lower()
            
            # Define scene settings based on genre
            genre_settings = {
                "fantasy": "magical realm with glowing crystals and ancient ruins",
                "sci-fi": "futuristic cityscape with neon lights and advanced technology",
                "mystery": "foggy street with dim streetlights and shadowy figures",
                "adventure": "vast landscape with distant mountains and unexplored terrain",
                "horror": "abandoned building with eerie shadows and decrepit furnishings",
                "romance": "sunset over a picturesque setting with soft, warm lighting",
                "western": "dusty frontier town with wooden buildings and desert landscape",
                "historical": "period-accurate setting with authentic architecture and attire",
                "thriller": "tense urban environment with stark contrasts and lurking danger",
                "comedy": "vibrant, slightly exaggerated scene with colorful elements"
            }
            
            # Define mood modifiers
            mood_modifiers = {
                "happy": "bright, warm colors, golden sunlight",
                "sad": "muted colors, blue tones, rain or mist",
                "tense": "sharp shadows, high contrast, red accents",
                "peaceful": "soft lighting, pastel colors, gentle atmosphere",
                "mysterious": "deep shadows, fog, limited visibility",
                "exciting": "dynamic composition, vibrant colors, motion blur",
                "scary": "dark shadows, desaturated colors, ominous lighting",
                "romantic": "soft focus, warm glow, intimate setting",
                "suspenseful": "dramatic lighting, high contrast, confined spaces",
                "melancholic": "faded colors, autumn tones, nostalgic atmosphere"
            }
            
            # Get setting based on genre or default
            genre = genre.lower()
            setting = genre_settings.get(genre, "atmospheric scene appropriate for the story")
            
            # Get mood modifier or default
            mood = mood.lower()
            mood_effect = mood_modifiers.get(mood, "appropriate atmospheric lighting")
            
            # Extract potential scene elements from the story text
            scene_elements = []
            
            # Look for key nouns that might indicate settings or objects
            potential_settings = ["castle", "forest", "mountain", "city", "village", "spaceship", 
                                  "sea", "ocean", "river", "house", "room", "cave", "laboratory", 
                                  "office", "mansion", "dungeon", "palace", "street", "desert", 
                                  "island", "battlefield", "garden", "temple", "church", "tower"]
            
            for place in potential_settings:
                if place in text:
                    scene_elements.append(place)
                    break
            
            # Look for time of day
            time_indicators = ["night", "day", "dawn", "dusk", "morning", "evening", "afternoon", "sunset", "sunrise"]
            for time in time_indicators:
                if time in text:
                    scene_elements.append(time)
                    break
            
            # Look for weather conditions
            weather_indicators = ["rain", "snow", "storm", "sunny", "cloudy", "fog", "mist", "thunder", "lightning"]
            for weather in weather_indicators:
                if weather in text:
                    scene_elements.append(weather)
                    break
            
            # Build the image prompt
            if scene_elements:
                scene_description = ", ".join(scene_elements)
                image_prompt = f"{scene_description} in a {setting} with {mood_effect}, featuring {character}"
            else:
                image_prompt = f"A {character} in a {setting} with {mood_effect}"
            
            # Add style guidance for consistency
            image_prompt += ", digital art, detailed, atmospheric lighting"
            
            return image_prompt
        except Exception as e:
            print(f"Error generating image prompt: {e}")
            return f"A scene from a {genre} story with {mood} mood featuring the main character"
    
    def _generate_image(self, prompt):
        """Generate an image based on the prompt using OpenAI's DALL-E"""
        try:
            response = openai.images.generate(
                model="dall-e-2",  # Using DALL-E 2 for faster generation
                prompt=prompt,
                n=1,
                size=self.image_size
            )
            
            # Return the URL of the generated image
            return response.data[0].url
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
