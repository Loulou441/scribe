"""
Module de transcription audio via l'API Speech-to-Text de Groq.
"""

import os
import json
from pathlib import Path
from groq import Groq, APIError, APIConnectionError, RateLimitError
from config import GROQ_API_KEY, STT_MODEL

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Specify the path to the audio file
filename = "audio_samples/test_audio_stt.mp4" # Replace with your audio file!

# Open the audio file
def transcription_from_audio(filename):
    path = Path(filename)
    if not path.is_file():
        raise FileNotFoundError(f"Fichier audio introuvable : {filename}") 
    try:
        with open(filename, "rb") as file:
            # Create a transcription of the audio file
            transcription = client.audio.transcriptions.create(
            file=file, # Required audio file
            model=STT_MODEL, # Required model to use for transcription
            prompt="Specify context or spelling",  # Optional
            response_format="verbose_json",  # Optional
            timestamp_granularities = ["word", "segment"], # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
            language="fr",  # Optional
            temperature=0.0  # Optional
            )
    except (APIError, APIConnectionError, RateLimitError) as e:
        raise RuntimeError(f"Échec de la transcription via l'API Groq : {e}") from e

    return transcription.text

if __name__ == "__main__":
    try:
        texte = transcription_from_audio(filename)
        print("Transcription :", texte)
    except FileNotFoundError as e:
        print(e)
    except RuntimeError as e:
        print(e)
