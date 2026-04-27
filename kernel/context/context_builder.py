"""
Execution Context Builder

Responsibilities:
- формирует execution context из Task
- определяет тип задачи
- вызывает Decision Layer (ModelRouter)
- (опционально) подключает RAG слой

Это НЕ RAG builder.
Это orchestrator уровня execution.

RAG — отдельный слой (kernel/rag)
"""

from kernel.execution.model_router import ModelRouter
from kernel.rag.context_builder import ContextBuilder as RAGContextBuilder


class ContextBuilder:
    """
    ContextBuilder — формирует execution context для задачи
    """

    def __init__(self):
        """
        Инициализация зависимостей
        """
        self.router = ModelRouter()

        # RAG builder (подключается по условию)
        self.rag_builder = RAGContextBuilder()

    # ------------------------------------------------------------------
    # BUILD CONTEXT
    # ------------------------------------------------------------------
    def build(self, task):
        """
        Формирует execution context

        :param task: объект Task
        :return: dict

        Структура context:
        {
            "task_id": str,
            "input": str,
            "task_type": str,
            "execution_type": str,
            "model": str,
            "rag_context": str
        }
        """

        # =========================
        # 1. Базовые данные
        # =========================
        context = {
            "task_id": task.id,
            "input": task.input_data,
        }

        # =========================
        # 2. Определение типа задачи
        # =========================
        context["task_type"] = self._detect_task_type(task.input_data)

        # =========================
        # 3. Routing (Decision Layer)
        # =========================
        route = self.router.route(context)

        context["execution_type"] = route["type"]
        context["model"] = route["model"]

        # =========================
        # 4. RAG Context (ВАЖНО)
        # =========================
        # Подключаем RAG только для задач выше simple
        if context["task_type"] in ["normal", "complex"]:
            rag_context = self.rag_builder.build(task.input_data)

            # защита от None / пустоты
            context["rag_context"] = rag_context if rag_context else ""

        else:
            context["rag_context"] = ""

        # =========================
        # 5. (ЗАДЕЛ НА БУДУЩЕЕ)
        # =========================
        # context["user"] = ...
        # context["history"] = ...
        # context["memory"] = ...

        return context

    # ------------------------------------------------------------------
    # TASK TYPE DETECTION
    # ------------------------------------------------------------------
    def _detect_task_type(self, input_text: str) -> str:
        """
        Определяет тип задачи

        :param input_text: текст запроса
        :return: simple | normal | complex
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
