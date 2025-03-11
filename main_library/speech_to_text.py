import os
import tempfile
import base64
import logging
import whisper
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*tokenizer.*")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv('key.env')

# Initialize Whisper model
whisper_model = whisper.load_model("tiny", device="cpu")

def speech_to_text(audio_data: bytes) -> dict:
    """
    Convert audio to text using Whisper.

    :param audio_data: The audio data as bytes
    :return: A dictionary containing the transcribed text and processing information
    """
    try:
        # Create a temporary file for the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_data)
            temp_audio_path = temp_audio.name

        # Transcribe the audio
        result = whisper_model.transcribe(temp_audio_path)
        transcribed_text = result['text']

        # Clean up the temporary file
        os.remove(temp_audio_path)

        return {
            "success": True,
            "text": transcribed_text,
            "model": "whisper-tiny"
        }
    except Exception as e:
        logger.error(f"STT Error: {e}")
        return {
            "success": False,
            "error": str(e)
        }

 