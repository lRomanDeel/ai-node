# kernel/execution/executor.py

class BaseExecutor:
    """
    Базовый интерфейс для всех executor'ов

    Это контракт, который должны реализовывать:
    - LLMExecutor
    - AgentExecutor (в будущем)
    - WorkflowExecutor (LangGraph)
    """

    async def run(self, context: dict):
        """
        Выполнение задачи

        :param context: execution context
        :return: результат выполнения
        """
        raise NotImplementedError("Executor must implement run()")
