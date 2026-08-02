# Enterprise AI Knowledge Copilot

Plateforme d'intelligence artificielle qui centralise la documentation
d'entreprise (PDF, Word...) et permet de l'interroger en langage naturel
via une API REST, avec citation systématique des sources.

Le système repose sur une architecture RAG (Retrieval Augmented Generation)
orchestrée par un graphe multi-agents (LangGraph), garantissant des réponses
fondées sur les documents réels de l'entreprise plutôt que sur les
connaissances générales du modèle de langage.

## Fonctionnalités

- **Questions en langage naturel** — interrogez la documentation via `POST /ask`
- **Ingestion manuelle** — upload de documents PDF/Word via l'API (réservé aux administrateurs)
- **Ingestion automatique** — surveillance d'un dossier OneDrive, détection des fichiers nouveaux ou modifiés (hash SHA-256)
- **Orchestration multi-agents** — 6 agents spécialisés avec branches conditionnelles :
  - `Planner` — filtre les échanges de politesse (pas de recherche inutile)
  - `Safety` — bloque les tentatives de prompt injection
  - `Retrieval` — recherche sémantique dans la base vectorielle
  - `Ranking` — filtre les résultats peu pertinents
  - `Answer` — génère la réponse à partir du contexte trouvé
  - `Citation` — déduplique et trie les sources citées
- **Authentification JWT** — routes sensibles protégées par rôle (admin/employee)
- **Traçabilité** — chaque réponse cite les documents et extraits utilisés, avec score de pertinence

## Stack technique

| Composant | Technologie |
|---|---|
| API | FastAPI + Pydantic v2 |
| Orchestration | LangGraph |
| LLM (génération) | Ollama — `qwen3:8b` |
| Embeddings | Ollama — `bge-m3` |
| Base vectorielle | ChromaDB |
| Base relationnelle | PostgreSQL + SQLAlchemy (async) |
| Ingestion cloud | Microsoft Graph API (OneDrive) |
| Authentification | JWT (python-jose) + bcrypt |
| Tests | Pytest (unitaires + intégration) |
| Qualité de code | Black, Ruff, MyPy |
| Conteneurisation | Docker / Docker Compose |
| CI/CD | GitHub Actions |

## Architecture du projet

app/
├── api/v1/routes/ # Endpoints HTTP (aucune logique métier)
├── core/ # Configuration, sécurité, dépendances FastAPI
├── services/ # Logique métier (ingestion, RAG, embeddings, hashing...)
├── agents/ # Agents LangGraph et graphe d'orchestration
├── models/ # Schémas Pydantic (contrats de données)
└── db/ # Accès PostgreSQL (SQLAlchemy) et ChromaDB
scripts/
├── init_db.py # Création des tables PostgreSQL
└── watch_onedrive.py # Watcher d'ingestion automatique OneDrive
tests/
├── unit/ # Tests de fonctions isolées
└── integration/ # Tests de l'API complète (TestClient)


L'API ne contient aucune logique métier : elle délègue systématiquement
aux services et aux agents. Cette séparation permet de réutiliser le même
pipeline d'ingestion pour l'upload manuel et le watcher automatique, sans
duplication de code.

## Prérequis

- Python 3.12+
- [Ollama](https://ollama.com) installé en local
- PostgreSQL 16+
- Docker et Docker Compose (pour un déploiement conteneurisé)

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

Éditez `.env` selon votre environnement (base de données, secret JWT,
identifiants Microsoft Graph si vous utilisez le watcher OneDrive).

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

### 6. (Optionnel) Lancer le watcher OneDrive

Pour activer l'ingestion automatique de documents déposés dans un dossier
OneDrive, configurez `MS_CLIENT_ID`, `MS_TENANT_ID` et `MS_CLIENT_SECRET`
dans `.env`, puis :

```bash
python scripts/watch_onedrive.py
```

## Démarrage avec Docker

Une seule commande suffit à lancer l'ensemble de la stack (API, PostgreSQL,
Redis, Ollama) :

```bash
docker compose up --build
```

Au premier lancement, téléchargez les modèles à l'intérieur du conteneur Ollama :

```bash
docker exec -it enterprise-ai-copilot-ollama-1 ollama pull bge-m3
docker exec -it enterprise-ai-copilot-ollama-1 ollama pull qwen3:8b
```

L'API est ensuite disponible sur http://localhost:8000, exactement comme
en développement local.

## Authentification

Deux comptes de démonstration sont disponibles :

| Utilisateur | Mot de passe | Rôle |
|---|---|---|
| `admin` | `admin123` | admin |
| `employe` | `user123` | employee |

Récupérez un token via `POST /api/v1/auth/login`, puis utilisez-le dans
le header `Authorization: Bearer <token>` pour accéder aux routes protégées
(comme `POST /api/v1/documents`).

## Tests

```bash
# Tests unitaires uniquement (rapides, aucune dépendance externe)
pytest tests/unit -v

# Suite complète (nécessite PostgreSQL et Ollama actifs)
pytest -v
```

## Qualité de code

```bash
black app tests           # Formatage
ruff check app tests      # Linting
mypy app                  # Vérification des types
```

Ces trois vérifications, ainsi que les tests unitaires, s'exécutent
automatiquement à chaque push via GitHub Actions (`.github/workflows/ci.yml`).

## Roadmap

- [x] API FastAPI versionnée
- [x] Pipeline RAG (extraction, chunking, embeddings, recherche sémantique)
- [x] Orchestration multi-agents LangGraph
- [x] Authentification JWT et gestion des rôles
- [x] Détection automatique de documents nouveaux/modifiés (hash + PostgreSQL)
- [x] Ingestion automatique depuis OneDrive (Microsoft Graph)
- [x] Tests unitaires et d'intégration
- [x] Dockerisation complète
- [x] CI/CD (GitHub Actions)
- [ ] Bascule vers un LLM cloud en production (Azure OpenAI / AWS Bedrock)
- [ ] Recherche fédérée sur d'autres sources (SharePoint, Confluence, GitHub)
- [ ] Reranking par modèle spécialisé
