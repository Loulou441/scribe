"""
Module de génération de compte rendu structuré à partir d'une transcription brute,
via le modèle LLM configuré.
"""

from pathlib import Path

from groq import Groq, APIError, APIConnectionError, RateLimitError

from config import GROQ_API_KEY, LLM_MODEL

from speech_to_text import transcription_from_audio

from formatteur_markdown import format_as_markdown, save_markdown_report

import json

client = Groq(api_key=GROQ_API_KEY)

PROMPT_PATH = Path(__file__).parent / "prompts_LLM" / "summary_generator_prompt.txt"


def _load_system_prompt() -> str:
    if not PROMPT_PATH.is_file():
        raise FileNotFoundError(f"Fichier de prompt système introuvable : {PROMPT_PATH}")
    return PROMPT_PATH.read_text(encoding="utf-8")


def generate_report(transcription: str) -> str:
    system_prompt = _load_system_prompt()

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            temperature=0.0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcription},
            ],
        )
    except (APIError, APIConnectionError, RateLimitError) as e:
        raise RuntimeError(
            f"Échec de la génération du compte rendu via l'API Groq : {e}"
        ) from e

    raw_content = response.choices[0].message.content
 
    try:
        report = json.loads(raw_content)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"La réponse du modèle n'est pas un JSON valide : {e}\nContenu reçu : {raw_content}"
        ) from e
 
    return report

if __name__ == "__main__":
    exemple = transcription_from_audio("audio_samples/test_audio_stt.mp4")
    try:
        compte_rendu = generate_report(exemple)
        md = format_as_markdown(compte_rendu)
        print(md)
        chemin = save_markdown_report(md)
    except (FileNotFoundError, RuntimeError) as e:
        print(e)