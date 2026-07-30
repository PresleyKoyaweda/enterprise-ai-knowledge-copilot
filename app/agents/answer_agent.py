import ollama

from app.core.config import settings
from app.agents.state import RAGState

client = ollama.Client(host=settings.ollama_base_url)


def _build_prompt(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)

    return f"""Tu es un assistant qui répond aux questions en te basant UNIQUEMENT sur le contexte fourni ci-dessous.
Si le contexte ne contient pas la réponse, dis clairement que tu ne sais pas.

Contexte :
{context}

Question : {question}

Réponse :"""


def answer_agent(state: RAGState) -> RAGState:
    prompt = _build_prompt(state["question"], state["context_chunks"])

    response = client.chat(
        model=settings.llm_model,
        messages=[{"role": "user", "content": prompt}],
    )

    state["answer"] = response["message"]["content"]

    return state