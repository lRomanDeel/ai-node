"""
BaseAgent — базовый класс для всех агентов системы.

Каждый агент:
- принимает данные (dict)
- возвращает данные (dict)
- не знает ничего о других агентах
"""

from typing import Dict, Any


class BaseAgent:
    """
    Базовый класс агента.

    Все агенты должны наследоваться от него
    и реализовывать метод run().
    """

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основной метод агента.

        :param data: входные данные
        :return: обработанные данные
        """
        raise NotImplementedError("Agent must implement run() method")