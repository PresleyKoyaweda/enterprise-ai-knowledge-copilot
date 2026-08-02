import ollama

from app.core.config import settings

client = ollama.Client(host=settings.ollama_base_url)


def embed_text(text: str) -> list[float]:
    response = client.embeddings(model=settings.embedding_model, prompt=text)
    return response["embedding"]


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    return [embed_text(chunk) for chunk in chunks]
