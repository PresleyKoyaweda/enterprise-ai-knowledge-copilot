from app.agents.state import RAGState

GREETING_PATTERNS = ["bonjour", "salut", "merci", "au revoir", "bonsoir", "hello"]


def _is_greeting(question: str) -> bool:
    normalized = question.lower().strip()
    return any(normalized.startswith(pattern) for pattern in GREETING_PATTERNS)


def planner_agent(state: RAGState) -> RAGState:
    question = state["question"]

    if _is_greeting(question):
        state["needs_rag"] = False
        state["direct_answer"] = (
            "Bonjour ! Je suis le copilote de connaissances de l'entreprise. "
            "Posez-moi une question sur la documentation interne et je ferai de mon mieux pour y répondre."
        )
        return state

    state["needs_rag"] = True
    state["direct_answer"] = ""
    return state
