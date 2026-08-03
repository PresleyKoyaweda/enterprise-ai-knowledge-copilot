from app.services.embedding_provider import get_embedding_provider


def embed_text(text: str) -> list[float]:
    provider = get_embedding_provider()
    return provider.embed(text)


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    return [embed_text(chunk) for chunk in chunks]
