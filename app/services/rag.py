import ollama

from app.core.config import settings
from app.db.vector_store import search
from app.services.embeddings import embed_text

client = ollama.Client(host=settings.ollama_base_url)


def _build_prompt(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)

    return f"""Tu es un assistant qui répond aux questions en te basant UNIQUEMENT sur le contexte fourni ci-dessous.
Si le contexte ne contient pas la réponse, dis clairement que tu ne sais pas.

Contexte :
{context}

Question : {question}

Réponse :"""


def answer_question(question: str, top_k: int = 5) -> tuple[str, list[dict]]:
    query_embedding = embed_text(question)

    results = search(query_embedding, top_k=top_k)

    context_chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    prompt = _build_prompt(question, context_chunks)

    response = client.chat(
        model=settings.llm_model,
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response["message"]["content"]

    sources = [
        {
            "document_name": metadatas[i]["document_id"],
            "excerpt": context_chunks[i][:200],
            "score": 1 - distances[i],
        }
        for i in range(len(context_chunks))
    ]

    return answer, sources
