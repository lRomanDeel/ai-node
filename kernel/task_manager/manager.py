# kernel/task_manager/manager.py

import uuid
from typing import Dict

from .models import Task, TaskStatus
from .state_machine import TaskStateMachine
from kernel.core.logger import logger


class TaskManager:
    """
    TaskManager — центральный компонент управления задачами.

    Отвечает за:
    - создание задач
    - хранение задач (в памяти, временно)
    - управление статусами (через FSM)
    - фиксацию результатов и ошибок

    В будущем:
    - будет подключён PostgreSQL
    - добавятся retry, priority, history
    """

    def __init__(self):
        """
        Инициализация TaskManager
        """

        # Временное хранилище задач (in-memory)
        # Формат: {task_id: Task}
        self.tasks: Dict[str, Task] = {}

        # Машина состояний (FSM)
        self.state_machine = TaskStateMachine()

        logger.info("[TASK MANAGER INIT] TaskManager initialized")

    def create_task(self, input_data: str) -> Task:
        """
        Создание новой задачи

        :param input_data: входные данные пользователя
        :return: объект Task
        """

        # Генерация уникального ID
        task_id = str(uuid.uuid4())

        # Создание задачи
        task = Task(
            id=task_id,
            input_data=input_data,
        )

        # Сохранение в хранилище
        self.tasks[task_id] = task

        # Логирование
        logger.info(f"[TASK CREATED] id={task_id} input='{input_data}'")

        return task

    def get_task(self, task_id: str) -> Task:
        """
        Получение задачи по ID

        :param task_id: ID задачи
        :return: Task
        """

        if task_id not in self.tasks:
            logger.error(f"[TASK NOT FOUND] id={task_id}")
            raise KeyError(f"Task {task_id} not found")

        return self.tasks[task_id]

    def set_status(self, task_id: str, new_status: TaskStatus):
        """
        Обновление статуса задачи с проверкой FSM

        :param task_id: ID задачи
        :param new_status: новый статус
        """

        task = self.get_task(task_id)

        old_status = task.status

        # Проверка допустимости перехода через FSM
        task.status = self.state_machine.transition(task.status, new_status)

        # Логирование перехода
        logger.info(
            f"[TASK STATUS] id={task_id} {old_status.value} → {new_status.value}"
        )

    def set_result(self, task_id: str, result):
        """
        Установка результата выполнения задачи

        :param task_id: ID задачи
        :param result: результат выполнения
        """

        task = self.get_task(task_id)

        task.result = result
        task.status = TaskStatus.COMPLETED

        logger.info(f"[TASK COMPLETED] id={task_id}")

    def set_error(self, task_id: str, error: str):
        """
        Фиксация ошибки выполнения задачи

        :param task_id: ID задачи
        :param error: текст ошибки
        """

        task = self.get_task(task_id)

        task.error = error
        task.status = TaskStatus.FAILED

        logger.error(f"[TASK FAILED] id={task_id} error={error}")
