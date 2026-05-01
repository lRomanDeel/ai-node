"""
IngestionAgent — отвечает за получение входных данных.

В MVP версии:
- принимает текст вручную
- нормализует вход
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class IngestionAgent(BaseAgent):
    """
    Агент получения данных.
    """

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Принимает входные данные и извлекает текст.

        :param data: входные данные (ожидается {"text": ...})
        :return: {"text": ...}
        """

        print("[IngestionAgent] Running...")

        text = data.get("text")

        # базовая валидация
        if not text:
            raise ValueError("No text provided to IngestionAgent")

        # нормализация (пока просто strip)
        text = text.strip()

        return {
            "text": text
        }