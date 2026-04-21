# kernel/task_manager/models.py

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


class TaskStatus(Enum):
    """
    Возможные состояния задачи (FSM)
    """
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """
    Основная модель задачи ядра
    """
    id: str
    input_data: str

    # Текущий статус задачи
    status: TaskStatus = TaskStatus.CREATED

    # Контекст выполнения (важно для расширения)
    context: Dict[str, Any] = field(default_factory=dict)

    # Результат выполнения
    result: Optional[Any] = None

    # Ошибка выполнения
    error: Optional[str] = None
