import ollama

from app.core.config import settings
from app.agents.state import RAGState
from app.prompts.loader import load_prompt

client = ollama.Client(host=settings.ollama_base_url)


def _build_prompt(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)
    template = load_prompt("answer_v1")

    return template.format(context=context, question=question)


def answer_agent(state: RAGState) -> RAGState:
    prompt = _build_prompt(state["question"], state["context_chunks"])

    response = client.chat(
        model=settings.llm_model,
        messages=[{"role": "user", "content": prompt}],
    )

    state["answer"] = response["message"]["content"]

    return state