from app.agents.state import RAGState
from app.prompts.loader import load_prompt

GREETING_PATTERNS = ["bonjour", "salut", "merci", "au revoir", "bonsoir", "hello"]

CAPABILITY_PATTERNS = [
    "que sais-tu faire",
    "que sais tu faire",
    "en quoi es-tu utile",
    "en quoi tu es utile",
    "à quoi tu sers",
    "a quoi tu sers",
    "c'est quoi ton rôle",
    "quel est ton rôle",
    "qui es-tu",
    "qui es tu",
    "que peux-tu faire",
    "que peux tu faire",
    "comment tu peux m'aider",
    "comment peux-tu m'aider",
]


def _is_greeting(question: str) -> bool:
    normalized = question.lower().strip()
    return any(normalized.startswith(pattern) for pattern in GREETING_PATTERNS)


def _is_capability_question(question: str) -> bool:
    normalized = question.lower().strip()
    return any(pattern in normalized for pattern in CAPABILITY_PATTERNS)


def planner_agent(state: RAGState) -> RAGState:
    question = state["question"]

    if _is_greeting(question) or _is_capability_question(question):
        state["needs_rag"] = False
        state["direct_answer"] = load_prompt("greeting_v1")
        return state

    state["needs_rag"] = True
    state["direct_answer"] = ""
    return state