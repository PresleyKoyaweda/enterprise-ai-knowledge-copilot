from app.agents.state import RAGState
from app.prompts.loader import load_prompt
from app.services.llm_provider import get_llm_provider


def _build_prompt(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)
    template = load_prompt("answer_v2")

    return template.format(context=context, question=question)


def answer_agent(state: RAGState) -> RAGState:
    prompt = _build_prompt(state["question"], state["context_chunks"])
    system_prompt = load_prompt("system_v1")

    provider = get_llm_provider()
    result = provider.generate(prompt, system_prompt=system_prompt)

    state["answer"] = result.text

    return state