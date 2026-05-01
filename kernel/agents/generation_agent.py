"""
GenerationAgent — отвечает за генерацию контента.

В MVP версии:
- формирует простой пост из текста
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class GenerationAgent(BaseAgent):
    """
    Агент генерации контента.
    """

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерирует пост.

        :param data: {"text": ...}
        :return: {"post": ...}
        """

        print("[GenerationAgent] Running...")

        text = data.get("text")

        if not text:
            raise ValueError("No text provided to GenerationAgent")

        # простая генерация (MVP)
        post = f"🔥 {text}\n\nПодписывайся на канал!"

        return {
            "post": post
        }