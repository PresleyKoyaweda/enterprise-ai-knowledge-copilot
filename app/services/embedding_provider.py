from abc import ABC, abstractmethod

import ollama
from huggingface_hub import InferenceClient

from app.core.config import settings


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]: ...


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self.client = ollama.Client(host=settings.ollama_base_url)

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings(model=settings.embedding_model, prompt=text)
        return response["embedding"]


class HuggingFaceEmbeddingProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self.client = InferenceClient(token=settings.hf_api_token)

    def embed(self, text: str) -> list[float]:
        result = self.client.feature_extraction(text, model="BAAI/bge-m3")
        return result.tolist()


def get_embedding_provider() -> EmbeddingProvider:
    if settings.embedding_provider == "huggingface":
        return HuggingFaceEmbeddingProvider()
    return OllamaEmbeddingProvider()