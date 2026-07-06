"""
Module de configuration centralisé du projet.
"""

from dotenv import load_dotenv
import os

# Charge les variables définies dans le fichier .env à la racine du projet
load_dotenv()

# --- Clé API ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY is None:
    raise ValueError(
        "GROQ_API_KEY introuvable. Vérifier son existance dans .env"
        "et qu'il contient une ligne : GROQ_API_KEY=..."
    )

# --- Identifiants des modèles ---
STT_MODEL = "whisper-large-v3-turbo" # Modèle de reconnaissance vocale (Speech-To-Text)
LLM_MODEL = "llama-3.1-8b-instant" # Modèle de langage (Large Language Model)