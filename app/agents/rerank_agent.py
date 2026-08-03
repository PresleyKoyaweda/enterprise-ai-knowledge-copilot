import re

from app.agents.state import RAGState
from app.prompts.loader import load_prompt
from app.services.llm_provider import get_llm_provider

TOP_N_AFTER_RERANK = 3


def _score_chunk(question: str, chunk: str) -> int:
    template = load_prompt("rerank_v1")
    prompt = template.format(question=question, chunk=chunk)

    provider = get_llm_provider()
    result = provider.generate(prompt)

    match = re.search(r"\d+", result.text)

    if not match:
        return 0

    score = int(match.group())
    return max(0, min(score, 10))


def rerank_agent(state: RAGState) -> RAGState:
    question = state["question"]
    chunks = state["context_chunks"]
    sources = state["sources_metadata"]

    scored = [
        (chunk, source, _score_chunk(question, chunk))
        for chunk, source in zip(chunks, sources)
    ]

    scored.sort(key=lambda item: item[2], reverse=True)

    top_items = scored[:TOP_N_AFTER_RERANK]

    state["context_chunks"] = [chunk for chunk, _, _ in top_items]
    state["sources_metadata"] = [
        {**source, "rerank_score": score} for _, source, score in top_items
    ]

    return state
