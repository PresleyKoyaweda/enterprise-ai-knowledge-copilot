from abc import ABC, abstractmethod

import ollama

from app.core.config import settings


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str: ...


class OllamaProvider(LLMProvider):
    def __init__(self) -> None:
        self.client = ollama.Client(host=settings.ollama_base_url)

    def generate(self, prompt: str) -> str:
        response = self.client.chat(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]


class GroqProvider(LLMProvider):
    def __init__(self) -> None:
        from groq import Groq

        self.client = Groq(api_key=settings.groq_api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content


def get_llm_provider() -> LLMProvider:
    if settings.llm_provider == "groq":
        return GroqProvider()
    return OllamaProvider()