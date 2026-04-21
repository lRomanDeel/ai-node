# kernel/context/context_builder.py

class ContextBuilder:
    """
    Формирует execution context для задачи
    """

    def build(self, task):
        """
        Создание контекста выполнения
        """

        return {
            "task_id": task.id,
            "input": task.input_data,
            "model": "llama3",
            "tools": [],
            "memory_refs": [],
            "params": {},
        }
