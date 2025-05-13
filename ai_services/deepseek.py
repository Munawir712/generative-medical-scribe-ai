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
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY environment variable is not set")

# API Configuration
DEEPSEEK_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek/deepseek-r1:free"

def generate_from_deepseek(prompt: str, include_reasoning: bool = True) -> str:
    """
    Generate text using Deepseek AI model.
    
    Args:
        prompt (str): The input prompt for the model
        include_reasoning (bool): Whether to include reasoning in the response
        
    Returns:
        str: The generated text response
        
    Raises:
        Exception: If there's an error during generation
    """
    try:
        logger.info("Preparing request to Deepseek API")
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Modify prompt based on reasoning preference
        if not include_reasoning:
            prompt = f"{prompt}\n\nPlease provide your response without any reasoning or explanation."
        
        payload = {
            "model": DEEPSEEK_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        logger.info("Sending request to Deepseek API")
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()

        if result.get("error"):
            raise Exception(f"Error from Deepseek: {result.get('error').get('message')}")
        
        if not result.get("choices"):
            raise Exception("No choices in Deepseek response")
            
        generated_text = result["choices"][0]["message"]["content"]
        if not generated_text:
            raise Exception("Empty response from Deepseek")
            
        logger.info("Successfully generated response from Deepseek")
        return generated_text
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {str(e)}")
        raise Exception(f"Failed to communicate with Deepseek API: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating from Deepseek: {str(e)}")
        raise Exception(f"Failed to generate response from Deepseek: {str(e)}")
