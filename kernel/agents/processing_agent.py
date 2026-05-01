"""
ProcessingAgent — отвечает за обработку текста.

В MVP версии:
- очистка текста
- минимальная нормализация
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class ProcessingAgent(BaseAgent):
    """
    Агент обработки текста.
    """

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обрабатывает текст.

        :param data: {"text": ...}
        :return: {"text": ...}
        """

        print("[ProcessingAgent] Running...")

        text = data.get("text")

        if not text:
            raise ValueError("No text provided to ProcessingAgent")

        # базовая обработка
        processed = text.strip()

        # можно добавить минимальную "логику"
        processed = " ".join(processed.split())

        return {
            "text": processed
        }