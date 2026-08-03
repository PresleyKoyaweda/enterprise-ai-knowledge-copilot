from abc import ABC, abstractmethod
from dataclasses import dataclass

import ollama

from app.core.config import settings


@dataclass
class LLMResult:
    text: str
    tokens_used: int | None = None


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str | None = None) -> LLMResult: ...


class OllamaProvider(LLMProvider):
    def __init__(self) -> None:
        self.client = ollama.Client(host=settings.ollama_base_url)

    def generate(self, prompt: str, system_prompt: str | None = None) -> LLMResult:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat(model=settings.llm_model, messages=messages)
        text = response["message"]["content"]
        tokens = response.get("eval_count")
        return LLMResult(text=text, tokens_used=tokens)


class GroqProvider(LLMProvider):
    def __init__(self) -> None:
        from groq import Groq

        self.client = Groq(api_key=settings.groq_api_key)

    def generate(self, prompt: str, system_prompt: str | None = None) -> LLMResult:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(model=settings.groq_model, messages=messages)  # type: ignore[arg-type]
        text = response.choices[0].message.content or ""
        tokens = response.usage.total_tokens if response.usage else None
        return LLMResult(text=text, tokens_used=tokens)


def get_llm_provider() -> LLMProvider:
    if settings.llm_provider == "groq":
        return GroqProvider()
    return OllamaProvider()