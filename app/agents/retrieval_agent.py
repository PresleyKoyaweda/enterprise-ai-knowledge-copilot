from app.agents.state import RAGState
from app.services.embeddings import embed_text
from app.db.vector_store import search


def retrieval_agent(state: RAGState) -> RAGState:
    question = state["question"]

    query_embedding = embed_text(question)
    results = search(query_embedding, top_k=5)

    state["context_chunks"] = results["documents"][0]
    state["sources_metadata"] = [
        {
            "document_name": results["metadatas"][0][i]["document_id"],
            "excerpt": results["documents"][0][i][:200],
            "score": 1 - results["distances"][0][i],
        }
        for i in range(len(results["documents"][0]))
    ]

    return state