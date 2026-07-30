from typing import TypedDict


class RAGState(TypedDict):
    question: str
    is_safe: bool
    rejection_reason: str
    context_chunks: list[str]
    sources_metadata: list[dict]
    answer: str