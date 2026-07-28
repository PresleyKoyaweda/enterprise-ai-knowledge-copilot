# Enterprise AI Knowledge Copilot

Plateforme IA qui centralise la documentation d'entreprise (PDF, Word,
PowerPoint, Excel...) et permet de l'interroger en langage naturel via
une API REST, avec citation des sources.

## Démarrage rapide

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
uvicorn app.main:app --reload
```

API disponible sur http://localhost:8000
Documentation interactive : http://localhost:8000/docs