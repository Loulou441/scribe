# Scribe

Scribe est un outil en ligne de commande qui transforme un enregistrement audio (réunion, cours, note vocale) en compte rendu écrit et structuré.

Il fonctionne en deux étapes :
1. **Transcription** : l'audio est converti en texte brut via un modèle Speech-to-Text.
2. **Compte rendu** : le texte brut est reformulé par un LLM en un compte rendu structuré (titre, points clés, décisions, actions).

Les deux modèles sont appelés via l'API serverless de [Groq](https://console.groq.com/docs/overview).

## Installation

```bash
git clone https://github.com/Loulou441/scribe
cd scribe
python -m venv .venv
source .venv/bin/activate  # sous Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Utilisation

```bash
python src/main.py
```

Le compte rendu s'affiche à l'écran et est sauvegardé dans un fichier Markdown daté.

## Structure du projet

```
scribe/
├── src/            # code source
├── audio_samples/  # fichiers audio
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Statut

Projet en cours de développement dans le cadre du TP M2 MD5 — Git, GitHub et intégration d'IA serverless.

## Question de réflexion

1. pourquoi le .gitignore doit-il exister avant d'écrire la moindre ligne de code
manipulant des secrets ?

Il est important de mettre en place le gitignore le plus rapidement possible dans le projet car cea permet d'éviter toute erreur de push. En effet, il est facile d'oublier de ne pas push certaines données importantes (ex: clé groq) lors de commit. Il convient don de les exclure dès le départ afin de ne plus s'en préoccuper.
