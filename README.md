# Conforma — Agent IA sur la Loi 25 (Québec)

Agent IA spécialisé en droit de la protection des renseignements personnels au
Québec (Loi 25). Le système répond en langage clair aux questions de conformité,
à partir de documents officiels, avec citation systématique des sources.

Le projet démontre une architecture complète de type "AI Engineer" : pipeline
RAG, orchestration multi-agents (LangGraph), sécurité, observabilité, et
déploiement cloud entièrement gratuit.

## Démo en ligne

- **Interface de chat** : https://enterprise-ai-knowledge-copilot-arkzk522ja9pefydfmrphx.streamlit.app
- **API + documentation Swagger** : https://enterprise-ai-copilot-api.onrender.com/docs

> ⚠️ L'API tourne sur un tier gratuit (Render) : le service se met en veille
> après 15 min d'inactivité — la première question après une pause peut
> prendre jusqu'à 60 secondes.

## Fonctionnalités

- **Questions en langage naturel** sur la Loi 25, avec sources citées et score de pertinence
- **Ingestion manuelle** de documents PDF/Word via l'API (réservée aux administrateurs)
- **Ingestion automatique** — surveillance d'un dossier OneDrive, détection des fichiers nouveaux/modifiés (hash SHA-256)
- **Orchestration multi-agents** (LangGraph), avec branches conditionnelles :
  - `Safety` — bloque les tentatives de prompt injection (s'exécute en premier, ne peut jamais être contourné)
  - `Planner` — classifie l'intention de la question par LLM (salutation / question sur l'agent / question de fond) plutôt que par une liste de mots-clés figée
  - `Retrieval` — recherche sémantique dans ChromaDB
  - `Ranking` — filtre les résultats peu pertinents par seuil de score
  - `Rerank` — note chaque résultat restant avec un LLM (LLM-as-reranker), ne garde que les meilleurs
  - `Answer` — génère la réponse avec un prompt système dédié (ton, style, règles de citation)
  - `Citation` — déduplique et trie les sources
- **Chunking hiérarchique** — découpe les documents par sections/paragraphes plutôt que par taille fixe, pour préserver le sens
- **Prompts versionnés** (`app/prompts/`) — jamais modifiés en place, toujours dupliqués en nouvelle version
- **Authentification JWT** — routes sensibles protégées par rôle (admin/employee)
- **Indépendance du fournisseur IA** — bascule Ollama (développement local) / Groq + Hugging Face (déploiement cloud gratuit) via une seule variable d'environnement

## Stack technique

| Composant | Développement local | Déploiement cloud (gratuit) |
|---|---|---|
| API | FastAPI + Pydantic v2 | Render (Docker) |
| Orchestration | LangGraph | — |
| Génération (LLM) | Ollama — `qwen3:8b` | Groq — `llama-3.3-70b-versatile` |
| Embeddings | Ollama — `bge-m3` | Hugging Face Inference — `BAAI/bge-m3` |
| Base vectorielle | ChromaDB (embarquée) | ChromaDB (embarquée, éphémère) |
| Base relationnelle | PostgreSQL local | Neon.tech (PostgreSQL managé) |
| Ingestion cloud | Microsoft Graph API (OneDrive) | — |
| Interface de chat | Streamlit (local) | Streamlit Community Cloud |
| Authentification | JWT (python-jose) + bcrypt | — |
| Tests | Pytest (unitaires + intégration) | — |
| Qualité de code | Black, Ruff, MyPy | — |
| CI/CD | — | GitHub Actions |

## Architecture du projet


app/
├── api/v1/routes/ # Endpoints HTTP (aucune logique métier)
├── core/ # Configuration, sécurité, dépendances FastAPI
├── services/ # Logique métier : ingestion, RAG, chunking hiérarchique,
│ # LLMProvider / EmbeddingProvider (abstraction fournisseur)
├── agents/ # Les 6 agents LangGraph + graphe d'orchestration
├── prompts/ # Prompts versionnés (system, answer, rerank, greeting...)
├── models/ # Schémas Pydantic (contrats de données)
└── db/ # Accès PostgreSQL (SQLAlchemy) et ChromaDB
scripts/
├── init_db.py # Création des tables PostgreSQL
└── watch_onedrive.py # Watcher d'ingestion automatique OneDrive
streamlit_app/
└── app.py # Interface de chat déployée sur Streamlit Cloud
tests/
├── unit/ # Tests de fonctions isolées
└── integration/ # Tests de l'API complète (TestClient)


L'API ne contient aucune logique métier : elle délègue systématiquement aux
services et aux agents. Le pipeline d'ingestion est identique, que le document
arrive par upload manuel ou par le watcher OneDrive.

## Prérequis (développement local)

- Python 3.12+
- [Ollama](https://ollama.com) installé en local
- PostgreSQL 16+
- Docker et Docker Compose (optionnel, pour un environnement conteneurisé complet)

## Démarrage rapide (développement local)

### 1. Cloner et installer

```bash
git clone https://github.com/PresleyKoyaweda/enterprise-ai-knowledge-copilot.git
cd enterprise-ai-knowledge-copilot

python3 -m venv .venv
source .venv/bin/activate   # Windows : .venv\Scripts\activate

pip install -e ".[dev]"
```

### 2. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Par défaut, `.env` est configuré pour Ollama en local (`LLM_PROVIDER=ollama`,
`EMBEDDING_PROVIDER=ollama`). Pour tester les fournisseurs cloud en local,
renseignez `GROQ_API_KEY` / `HF_API_TOKEN` et changez les providers.

### 3. Démarrer les modèles Ollama

```bash
ollama serve
ollama pull bge-m3
ollama pull qwen3:8b
```

### 4. Initialiser la base de données

```bash
createdb copilot
python scripts/init_db.py
```

### 5. Lancer l'API

```bash
uvicorn app.main:app --reload
```

- API : http://localhost:8000
- Documentation interactive (Swagger) : http://localhost:8000/docs

### 6. Lancer l'interface de chat en local

```bash
pip install streamlit
streamlit run streamlit_app/app.py
```

L'interface locale appelle par défaut l'API en production (Render) — modifiez
`API_BASE_URL` dans `streamlit_app/app.py` pour pointer vers votre API locale
si besoin.

### 7. (Optionnel) Lancer le watcher OneDrive

```bash
python scripts/watch_onedrive.py
```

Nécessite `MS_CLIENT_ID`, `MS_TENANT_ID` et `MS_CLIENT_SECRET` dans `.env`.

## Démarrage avec Docker (environnement local complet)

```bash
docker compose up --build
```

Au premier lancement, téléchargez les modèles dans le conteneur Ollama :

```bash
docker exec -it enterprise-ai-copilot-ollama-1 ollama pull bge-m3
docker exec -it enterprise-ai-copilot-ollama-1 ollama pull qwen3:8b
```

## Authentification

| Utilisateur | Mot de passe | Rôle |
|---|---|---|
| `admin` | `admin123` | admin |
| `employe` | `user123` | employee |

Récupérez un token via `POST /api/v1/auth/login`, puis utilisez-le dans le
header `Authorization: Bearer <token>` pour accéder aux routes protégées.

## Tests

```bash
# Tests unitaires uniquement (rapides, aucune dépendance externe)
pytest tests/unit -v

# Suite complète (nécessite PostgreSQL et Ollama actifs)
pytest -v
```

## Qualité de code

```bash
black app tests
ruff check app tests
mypy app
```

Ces vérifications, ainsi que les tests unitaires, s'exécutent automatiquement
à chaque push via GitHub Actions (`.github/workflows/ci.yml`).

## Limites connues (déploiement gratuit)

- **ChromaDB est stockée dans le système de fichiers du conteneur Render** —
  chaque redémarrage (mise en veille après inactivité, nouveau déploiement)
  vide la base vectorielle. Les documents doivent être réingérés après un
  redémarrage. *(Une solution de réingestion automatique au démarrage est en cours.)*
- Le plan gratuit Render dispose de 512 Mo de RAM / 0.1 CPU — largement
  suffisant depuis la bascule vers des fournisseurs LLM/embeddings cloud
  (Groq, Hugging Face), mais impose un traitement séquentiel (pas de
  parallélisation des embeddings à l'ingestion).

## Roadmap

- [x] API FastAPI versionnée
- [x] Pipeline RAG (extraction, chunking hiérarchique, embeddings, recherche sémantique, reranking)
- [x] Orchestration multi-agents LangGraph (6 agents)
- [x] Authentification JWT et gestion des rôles
- [x] Détection automatique de documents nouveaux/modifiés (hash + PostgreSQL)
- [x] Ingestion automatique depuis OneDrive (Microsoft Graph)
- [x] Tests unitaires et d'intégration
- [x] Dockerisation complète (développement local)
- [x] CI/CD (GitHub Actions)
- [x] Indépendance du fournisseur IA (LLMProvider / EmbeddingProvider)
- [x] Déploiement cloud gratuit (Render + Neon + Groq + Hugging Face)
- [x] Interface de chat (Streamlit) déployée publiquement
- [x] Prompt système et personnalité cohérente de l'agent
- [ ] Réingestion automatique des documents de référence au démarrage
- [ ] Génération en streaming (réponse progressive côté interface)
- [ ] Back-office (logs, temps de réponse, gestion des documents)