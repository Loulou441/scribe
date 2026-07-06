"""
Module depipeline complète pour le projet Scribe
"""

import sys

from speech_to_text import transcription_from_audio
from summary import generate_report
from formatteur_markdown import format_as_markdown, save_markdown_report


def main():
    if len(sys.argv) != 2:
        print("Usage : python src/main.py <chemin_vers_fichier_audio>")
        sys.exit(1)
 
    audio_path = sys.argv[1]

    # Étape 1 : transcription
    print(f"🎙️  Transcription en cours... ({audio_path})")
    try:
        texte = transcription_from_audio(audio_path)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"❌ Erreur lors de la transcription : {e}")
        sys.exit(1)
    print("✅ Transcription terminée.")

    # Étape 2 : compte rendu structuré
    print("✍️  Rédaction du compte rendu en cours...")
    try:
        report = generate_report(texte)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"❌ Erreur lors de la génération du compte rendu : {e}")
        sys.exit(1)
    print("✅ Compte rendu généré.")

    # Étape 3 : mise en forme et sauvegarde
    markdown = format_as_markdown(report)

    chemin = save_markdown_report(markdown)
    print(f"💾 Compte rendu sauvegardé dans : {chemin}")


if __name__ == "__main__":
    main()