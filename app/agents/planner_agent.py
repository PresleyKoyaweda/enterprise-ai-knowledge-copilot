from app.agents.state import RAGState
from app.prompts.loader import load_prompt
from app.services.llm_provider import get_llm_provider


def _classify_intent(question: str) -> str:
    template = load_prompt("intent_classifier_v1")
    prompt = template.format(question=question)

    provider = get_llm_provider()
    result = provider.generate(prompt)

    intent = result.text.strip().lower()

    if intent not in ("greeting", "capability", "content"):
        return "content"

    return intent


def _build_greeting_answer() -> str:
    base_message = load_prompt("greeting_v1")
    template = load_prompt("greeting_reformulation_v1")
    prompt = template.format(base_message=base_message)
    system_prompt = load_prompt("system_v1")

    provider = get_llm_provider()
    result = provider.generate(prompt, system_prompt=system_prompt)

    return result.text


def planner_agent(state: RAGState) -> RAGState:
    question = state["question"]
    intent = _classify_intent(question)

    if intent in ("greeting", "capability"):
        state["needs_rag"] = False
        state["direct_answer"] = _build_greeting_answer()
        return state

    state["needs_rag"] = True
    state["direct_answer"] = ""
    return state
