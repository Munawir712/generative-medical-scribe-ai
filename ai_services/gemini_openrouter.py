import requests
import os
from dotenv import load_dotenv
import logging
from typing import Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")

# API Configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
GEMINI_MODEL = "google/gemini-2.0-flash-exp:free"

def generate_from_gemini(prompt: str) -> str:
    """
    Generate text using Gemini AI model through OpenRouter API.
    
    Args:
        prompt (str): The input prompt for the model
        
    Returns:
        str: The generated text response
        
    Raises:
        Exception: If there's an error during generation
    """
    try:
        logger.info("Preparing request to OpenRouter API for Gemini")
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://medical-scribe-ai-api.com",  # Replace with your actual domain
            "X-Title": "Medical Scribe AI API"  # Your application name
        }
        
        payload = {
            "model": GEMINI_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        logger.info("Sending request to OpenRouter API")
        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        if not result.get("choices"):
            raise Exception("No choices in Gemini response")
            
        generated_text = result["choices"][0]["message"]["content"]
        if not generated_text:
            raise Exception("Empty response from Gemini")
            
        logger.info("Successfully generated response from Gemini")
        return generated_text
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {str(e)}")
        raise Exception(f"Failed to communicate with OpenRouter API: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating from Gemini: {str(e)}")
        raise Exception(f"Failed to generate response from Gemini: {str(e)}") 