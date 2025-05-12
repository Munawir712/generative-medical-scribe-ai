import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def generate_from_gemini(prompt: str) -> str:
    """
    Generate text using Google's Gemini AI model.
    
    Args:
        prompt (str): The input prompt for the model
        
    Returns:
        str: The generated text response
        
    Raises:
        Exception: If there's an error during generation
    """
    try:
        logger.info("Initializing Gemini model")
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        logger.info("Generating response from Gemini")
        response = model.generate_content(prompt)
        
        if not response.text:
            raise Exception("Empty response from Gemini")
            
        logger.info("Successfully generated response from Gemini")
        return response.text
        
    except Exception as e:
        logger.error(f"Error generating from Gemini: {str(e)}")
        raise Exception(f"Failed to generate response from Gemini: {str(e)}")
