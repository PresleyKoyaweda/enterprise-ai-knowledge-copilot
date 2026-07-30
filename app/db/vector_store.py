import chromadb

from app.core.config import settings


client = chromadb.PersistentClient(path=settings.chroma_persist_dir)

collection = client.get_or_create_collection(
    name=settings.chroma_collection_name,
    metadata={"hnsw:space": "cosine"},
)


def add_chunks(document_id: str, chunks: list[str], embeddings: list[list[float]]) -> None:
    ids = [f"{document_id}_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"document_id": document_id} for _ in chunks],
    )


def search(query_embedding: list[float], top_k: int = 5) -> dict:
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )