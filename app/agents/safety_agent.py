from app.agents.state import RAGState

SUSPICIOUS_PATTERNS = [
    "ignore les instructions",
    "ignore tes instructions",
    "oublie tes instructions",
    "system prompt",
    "tu es maintenant",
]


def _is_prompt_injection_attempt(question: str) -> bool:
    normalized = question.lower()
    return any(pattern in normalized for pattern in SUSPICIOUS_PATTERNS)


def safety_agent(state: RAGState) -> RAGState:
    question = state["question"]

    if _is_prompt_injection_attempt(question):
        state["is_safe"] = False
        state["rejection_reason"] = (
            "La question contient une tentative de manipulation du système."
        )
        return state

    state["is_safe"] = True
    state["rejection_reason"] = ""
    return state
