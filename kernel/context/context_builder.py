# kernel/context/context_builder.py

from kernel.execution.model_router import ModelRouter


class ContextBuilder:
    """
    ContextBuilder — формирует execution context для задачи.

    Архитектурная роль:
    - изолирует подготовку данных от логики выполнения
    - формирует единый объект context (единая точка правды)
    - подключает Decision Layer (ModelRouter)

    Контекст используется:
    - Coordinator → передаёт в Executor
    - Router → принимает решение
    - Executor → выполняет задачу

    В будущем сюда добавится:
    - RAG (документы из векторной БД)
    - user context (пользователь, тариф, настройки)
    - history / memory
    - system prompts
    """

    def __init__(self):
        """
        Инициализация builder'а
        """
        self.router = ModelRouter()

    def build(self, task):
        """
        Формирует execution context

        :param task: объект Task
        :return: dict (execution context)

        Пример структуры:
        {
            "task_id": str,
            "input": str,
            "task_type": str,
            "execution_type": "local" | "api",
            "model": str
        }
        """

        # =========================
        # 1. Базовые данные задачи
        # =========================
        context = {
            "task_id": task.id,
            "input": task.input_data,
        }

        # =========================
        # 2. Определение типа задачи
        # =========================
        # Пока используем простую эвристику
        # (длина текста)
        context["task_type"] = self._detect_task_type(task.input_data)

        # =========================
        # 3. Routing (Decision Layer)
        # =========================
        route = self.router.route(context)

        context["execution_type"] = route["type"]
        context["model"] = route["model"]

        # =========================
        # 4. (Задел) дополнительные поля
        # =========================
        # сюда позже добавим:
        # context["documents"] = ...
        # context["user"] = ...
        # context["history"] = ...

        return context

    def _detect_task_type(self, input_text: str) -> str:
        """
        Определяет тип задачи

        :param input_text: текст запроса
        :return: task_type (simple | normal | complex)

        Текущая логика (MVP):
        - короткий текст → simple
        - средний → normal
        - длинный → complex

        В будущем:
        - NLP классификация
        - intent detection
        - бизнес-правила
        """

        if not input_text:
            return "simple"

        length = len(input_text)

        if length < 100:
            return "simple"

        elif length < 500:
            return "normal"

        else:
            return "complex"
