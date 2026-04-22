# kernel/core/metrics.py

import time
from collections import defaultdict
from threading import Lock


class Metrics:
    """
    Metrics — слой наблюдаемости (Observability Layer)

    Отвечает за:
    - счётчики событий (tasks_completed, errors и т.д.)
    - тайминги выполнения задач
    - базовую аналитику производительности

    ВАЖНО:
    Это in-memory реализация (MVP)

    В будущем:
    - Prometheus
    - Grafana
    - external monitoring systems
    """

    def __init__(self):
        # счётчики (events)
        self.counters = defaultdict(int)

        # список длительностей задач
        self.timings = []

        # блокировка для thread-safety
        self._lock = Lock()

    # =========================
    # COUNTERS
    # =========================
    def inc(self, name: str, value: int = 1):
        """
        Увеличить счётчик

        :param name: имя метрики (например "completed")
        :param value: на сколько увеличить
        """
        with self._lock:
            self.counters[name] += value

    # =========================
    # TIMINGS
    # =========================
    def add_timing(self, duration: float):
        """
        Добавить время выполнения задачи

        :param duration: время в секундах
        """
        with self._lock:
            self.timings.append(duration)

    # =========================
    # SNAPSHOT
    # =========================
    def snapshot(self) -> dict:
        """
        Получить текущее состояние метрик

        :return: dict с метриками
        """

        with self._lock:
            total_tasks = len(self.timings)

            avg_duration = (
                sum(self.timings) / total_tasks
                if total_tasks > 0
                else 0
            )

            max_duration = max(self.timings) if self.timings else 0
            min_duration = min(self.timings) if self.timings else 0

            return {
                "counters": dict(self.counters),
                "total_tasks": total_tasks,
                "avg_duration": round(avg_duration, 4),
                "max_duration": round(max_duration, 4),
                "min_duration": round(min_duration, 4),
            }

    # =========================
    # RESET (для тестов)
    # =========================
    def reset(self):
        """
        Сброс метрик (используется в тестах)
        """
        with self._lock:
            self.counters.clear()
            self.timings.clear()


# =========================
# Глобальный singleton
# =========================

metrics = Metrics()