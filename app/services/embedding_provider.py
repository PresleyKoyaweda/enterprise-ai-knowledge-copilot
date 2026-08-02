from abc import ABC, abstractmethod

import ollama
import requests

from app.core.config import settings

HF_API_URL = "https://api-inference.huggingface.co/models/BAAI/bge-m3"


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
        self.headers = {"Authorization": f"Bearer {settings.hf_api_token}"}

    def embed(self, text: str) -> list[float]:
        response = requests.post(
            HF_API_URL,
            headers=self.headers,
            json={"inputs": text},
        )
        response.raise_for_status()
        return response.json()


def get_embedding_provider() -> EmbeddingProvider:
    if settings.embedding_provider == "huggingface":
        return HuggingFaceEmbeddingProvider()
    return OllamaEmbeddingProvider()