# kernel/task_manager/state_machine.py

from .models import TaskStatus


class InvalidTransition(Exception):
    """Ошибка некорректного перехода состояния"""
    pass


class TaskStateMachine:
    """
    Управляет переходами состояний задач
    """

    allowed_transitions = {
        TaskStatus.CREATED: [TaskStatus.QUEUED],
        TaskStatus.QUEUED: [TaskStatus.RUNNING],
        TaskStatus.RUNNING: [
            TaskStatus.WAITING,
            TaskStatus.COMPLETED,
            TaskStatus.FAILED,
        ],
        TaskStatus.WAITING: [
            TaskStatus.RUNNING,
            TaskStatus.FAILED,
        ],
    }

    def transition(self, current: TaskStatus, new: TaskStatus) -> TaskStatus:
        """
        Проверяет и выполняет переход состояния
        """
        if new not in self.allowed_transitions.get(current, []):
            raise InvalidTransition(f"{current} → {new} not allowed")

        return new
