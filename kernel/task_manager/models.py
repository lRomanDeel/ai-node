# kernel/task_manager/models.py

from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import uuid


class TaskStatus(str, Enum):
    """
    TaskStatus — жизненный цикл задачи (FSM).

    Используется Kernel'ом для управления состоянием задачи.

    Поток состояний:

    QUEUED → RUNNING → COMPLETED
                    → FAILED
                    → TIMEOUT

    Дополнительно:
    RETRYING — промежуточное состояние при повторной попытке
    """

    QUEUED = "queued"        # задача создана и ожидает выполнения
    RUNNING = "running"      # задача выполняется
    RETRYING = "retrying"    # выполняется повторная попытка
    COMPLETED = "completed"  # успешно завершена
    FAILED = "failed"        # завершена с ошибкой
    TIMEOUT = "timeout"      # превышено время выполнения


@dataclass
class Task:
    """
    Task — основная сущность Kernel'а.

    Хранит:
    - входные данные
    - статус
    - результат
    - ошибку
    - контекст выполнения (trace, routing и т.д.)

    ВАЖНО:
    Task — это "контейнер состояния", а не логика.
    """

    id: str
    input_data: str

    # текущее состояние задачи
    status: TaskStatus = TaskStatus.QUEUED

    # результат выполнения (если успешно)
    result: Optional[Any] = None

    # текст ошибки (если была)
    error: Optional[str] = None

    # дополнительный контекст (trace, routing, metadata)
    context: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def create(input_data: str) -> "Task":
        """
        Фабричный метод создания задачи

        :param input_data: входные данные
        :return: Task
        """

        return Task(
            id=str(uuid.uuid4()),  # уникальный ID задачи
            input_data=input_data
        )