from typing import TypedDict


class RAGState(TypedDict):
    question: str
    is_safe: bool
    rejection_reason: str
    needs_rag: bool
    direct_answer: str
    context_chunks: list[str]
    sources_metadata: list[dict]
    has_relevant_context: bool
    answer: str