"""
Base LLM Client

Контракт для всех моделей
"""

class BaseLLMClient:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError
