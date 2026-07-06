"""
Module de mise en forme du compte rendu : transforme le dict JSON renvoyé en un Markdown daté et lisible.
"""

from datetime import datetime
from pathlib import Path


def format_as_markdown(report: dict) -> str:
    """
    Convertit un compte rendu structuré (dict JSON) en Markdown daté et lisible.
    """
    date_str = datetime.now().strftime("%d/%m/%Y à %H:%M")

    titre = report.get("titre", "Compte rendu").strip()
    resume = report.get("resume", "").strip()
    points_cles = report.get("points_cles", [])
    decisions_actions = report.get("decisions_actions", [])

    lignes = [
        f"# {titre}",
        "",
        f"*Généré le {date_str} par Scribe*",
        "",
        "---",
        "",
        "## 📝 Résumé",
        "",
        resume,
        "",
        "## 🔑 Points clés",
        "",
    ]

    if points_cles:
        lignes += [f"- {point}" for point in points_cles]
    else:
        lignes.append("*Aucun point clé identifié.*")

    lignes += ["", "## ✅ Décisions et actions", ""]

    if decisions_actions:
        lignes += [f"- {item}" for item in decisions_actions]
    else:
        lignes.append("*Aucune décision ou action explicite mentionnée dans cet enregistrement.*")

    lignes.append("")

    return "\n".join(lignes)


def save_markdown_report(markdown_text: str, output_dir: str = "comptes_rendus") -> Path:
    """
    Sauvegarde un compte rendu Markdown dans un fichier daté.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filename = f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}_compte-rendu.md"
    filepath = output_path / filename
    filepath.write_text(markdown_text, encoding="utf-8")

    return filepath


if __name__ == "__main__":
    exemple_report = {
        "titre": "Point d'avancement projet Scribe",
        "resume": "L'équipe a fait le point sur l'avancement du module de transcription. Le modèle whisper-large-v3-turbo est confirmé pour la production. Le passage au JSON mode pour le LLM a été validé.",
        "points_cles": [
            "whisper-large-v3-turbo retenu pour la transcription",
            "Le module de compte rendu utilise désormais le JSON mode de Groq",
        ],
        "decisions_actions": [],
    }
    md = format_as_markdown(exemple_report)
    print(md)
    chemin = save_markdown_report(md)
    print(f"\nSauvegardé dans : {chemin}")