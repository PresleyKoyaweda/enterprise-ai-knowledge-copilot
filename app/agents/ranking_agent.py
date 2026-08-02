from app.agents.state import RAGState

MIN_RELEVANCE_SCORE = 0.5


def ranking_agent(state: RAGState) -> RAGState:
    filtered_chunks = []
    filtered_sources = []

    for chunk, source in zip(state["context_chunks"], state["sources_metadata"]):
        if source["score"] >= MIN_RELEVANCE_SCORE:
            filtered_chunks.append(chunk)
            filtered_sources.append(source)

    state["context_chunks"] = filtered_chunks
    state["sources_metadata"] = filtered_sources
    state["has_relevant_context"] = len(filtered_chunks) > 0

    return state
