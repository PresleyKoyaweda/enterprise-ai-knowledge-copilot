from app.agents.state import RAGState


def _deduplicate_and_sort(sources: list[dict]) -> list[dict]:
    sorted_sources = sorted(sources, key=lambda s: s["score"], reverse=True)

    seen_documents = set()
    unique_sources = []

    for source in sorted_sources:
        document_name = source["document_name"]

        if document_name not in seen_documents:
            seen_documents.add(document_name)
            unique_sources.append(source)

    return unique_sources


def citation_agent(state: RAGState) -> RAGState:
    state["sources_metadata"] = _deduplicate_and_sort(state["sources_metadata"])
    return state