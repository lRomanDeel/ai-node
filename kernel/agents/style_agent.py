"""
StyleAgent — отвечает за оформление поста.

В MVP версии:
- добавляет хештеги
- делает финальную полировку
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class StyleAgent(BaseAgent):
    """
    Агент стилизации контента.
    """

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Оформляет пост.

        :param data: {"post": ...}
        :return: {"post": ...}
        """

        print("[StyleAgent] Running...")

        post = data.get("post")

        if not post:
            raise ValueError("No post provided to StyleAgent")

        # добавляем стиль
        styled_post = post + "\n\n#crypto #bitcoin #AI"

        return {
            "post": styled_post
        }