# kernel/core/timing.py

import time


class Timer:
    """
    Универсальный таймер для измерения времени выполнения.

    Используется для:
    - общего времени задачи
    - отдельных этапов (executor, context и т.д.)
    """

    def __init__(self):
        # Время старта
        self.start_time = time.perf_counter()

        # Метки этапов
        self.marks = {}

    def mark(self, name: str):
        """
        Фиксирует время для конкретного этапа

        :param name: название этапа
        """
        self.marks[name] = time.perf_counter()

    def get_duration(self, name: str) -> float:
        """
        Возвращает длительность этапа (с момента старта)

        :param name: имя этапа
        :return: время в секундах
        """
        if name not in self.marks:
            return 0.0

        return self.marks[name] - self.start_time

    def total(self) -> float:
        """
        Общее время выполнения

        :return: время в секундах
        """
        return time.perf_counter() - self.start_time
