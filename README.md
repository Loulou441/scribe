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

### Transcription audio (Speech-to-Text)

La transcription est gérée par `src/speech_to_text.py`, qui appelle le modèle STT de Groq (`STT_MODEL` défini dans `config.py`, actuellement `whisper-large-v3-turbo`).

```python
from speech_to_text import transcription_from_audio

texte = transcription_from_audio("audio_samples/mon_fichier.wav")
print(texte)
```

**Formats audio acceptés par l'API Groq** : `flac`, `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `ogg`, `wav`, `webm`

**Taille maximale** : 25 Mo (tier gratuit) / 100 Mo (tier payant)

**Gestion des erreurs** :
- `FileNotFoundError` si le chemin du fichier audio n'existe pas
- `RuntimeError` si l'appel à l'API Groq échoue (réseau, quota dépassé, erreur serveur...)

Un échantillon audio léger (~30 secondes) est disponible dans `audio_samples/` pour tester la fonction sans avoir à enregistrer sa propre voix.

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

2. Quels modèles STT et LLM propose Groq aujourd'hui, et lesquels choisissez-vous ? Justifiez (qualité, vitesse, coût) dans le README.

- Le STT
Aujourd'hui, Groq propose deux modèles, `whisper-large-v3` et `whisper-large-v3-turbo`. Si on en croit la documentation, la différence entre les deux au niveau du WER est minime, pour un prix plus élevé et une vitesse plus lente au niveau de `whisper-large-v3`. 
Nous prendrons donc `whisper-large-v3-turbo` pour ce projet.

- Le LLM
Pour ce qui est du LLM, Groq propose de nombreux modèes comme `llama-3.1-8b-instant`, `llama-3.3-70b-versatile`, `openai/gpt-oss-20b` ou encore `openai/gpt-oss-120b`. Pour la tâche simple qui est de transformer la sortie brute du STT en rapport, `llama-3.1-8b-instant` est le plus adapté selon le rapport prix/ efficacité sur ce type de tâches.

3. Que renvoie exactement l'API en plus du texte (langue détectée, segments, horodatage...) ? Qu'est-ce qui pourrait être utile pour une évolution future de Scribe ?

Selon la documentation de Groq, la réponse contient, en plus du texte (`text`) dans le json de sortie donc il y a un exemple juste dessous:

```json
{
  "id": 8,
  "seek": 3000,
  "start": 43.92,
  "end": 50.16,
  "text": "document that the functional specification that you started to read through that isn't just the",
  "tokens": [51061, 4166, 300, 264, 11745, 31256],
  "temperature": 0,
  "avg_logprob": -0.097569615,
  "compression_ratio": 1.6637554,
  "no_speech_prob": 0.012814695
}
```
 
| Champ | Signification |
|---|---|
| `id` | numéro du segment dans l'audio |
| `seek` | position interne utilisée par le modèle (en centièmes de seconde) |
| `start` / `end` | horodatage de début/fin du segment, en secondes |
| `text` | texte transcrit pour ce segment |
| `tokens` | tokens internes du modèle (peu utile en pratique) |
| `temperature` | valeur de température utilisée pour ce segment (0 = déterministe) |
| `avg_logprob` | confiance moyenne du modèle sur ce segment (proche de 0 = bonne confiance) |
| `compression_ratio` | détecte les répétitions/bégaiements anormaux (valeur normale ≈ 1–2) |
| `no_speech_prob` | probabilité qu'il n'y ait pas de parole dans ce segment (silence, musique...) |
