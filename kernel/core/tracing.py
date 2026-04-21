# kernel/core/tracing.py

import time
from typing import List, Dict, Any


class Span:
    """
    Span — отдельный шаг выполнения (например: executor, context)
    """

    def __init__(self, name: str):
        self.name = name
        self.start_time = time.perf_counter()
        self.end_time = None
        self.duration = None
        self.metadata: Dict[str, Any] = {}

    def finish(self):
        """Завершение span"""
        self.end_time = time.perf_counter()
        self.duration = self.end_time - self.start_time

    def set_metadata(self, key: str, value: Any):
        """Добавление метаданных"""
        self.metadata[key] = value

    def to_dict(self):
        """Сериализация"""
        return {
            "name": self.name,
            "duration": round(self.duration, 6) if self.duration else None,
            "metadata": self.metadata,
        }


class Trace:
    """
    Trace — цепочка выполнения задачи
    """

    def __init__(self, task_id: str):
        self.task_id = task_id
        self.start_time = time.perf_counter()
        self.spans: List[Span] = []

    def start_span(self, name: str) -> Span:
        """Создать новый span"""
        span = Span(name)
        self.spans.append(span)
        return span

    def total_duration(self):
        """Общее время выполнения"""
        return time.perf_counter() - self.start_time

    def to_dict(self):
        """Сериализация всей трассировки"""
        return {
            "task_id": self.task_id,
            "total_duration": round(self.total_duration(), 6),
            "spans": [span.to_dict() for span in self.spans],
        }
