import os
import tempfile
import base64
import logging
import re
from flask import Flask, request, jsonify
from gtts import gTTS
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv('key.env')

def preprocess_text(text: str) -> str:
    """
    Clean and format text for TTS.
    
    :param text: The input text to process
    :return: Processed text ready for TTS
    """
    text = re.sub(r'\s+', ' ', text).strip()
    if not text.endswith(('.', '!', '?')):
        text += '.'
    return text

def text_to_speech(text: str, lang: str = 'en') -> dict:
    """
    Convert text to speech using gTTS.
    
    :param text: The text to convert to speech
    :param lang: The language code (default: 'en')
    :return: A dictionary containing the base64 encoded audio and metadata
    """
    try:
        processed_text = preprocess_text(text)
        
        # Create temporary file for the audio
        tts_output_path = tempfile.mktemp(suffix=".mp3")
        
        # Generate speech
        tts = gTTS(text=processed_text, lang=lang)
        tts.save(tts_output_path)
        
        # Read and encode the audio file
        with open(tts_output_path, 'rb') as audio_file:
            audio_data = audio_file.read()
            response_audio = base64.b64encode(audio_data).decode('utf-8')
        
        # Clean up the temporary file
        os.remove(tts_output_path)
        
        return {
            "success": True,
            "audio_base64": response_audio,
            "format": "mp3",
            "language": lang,
            "text_length": len(processed_text)
        }
    except Exception as e:
        logger.error(f"TTS Error: {e}")
        return {
            "success": False,
            "error": str(e)
        }
