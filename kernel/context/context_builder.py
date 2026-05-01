"""
Context Builder (Stage 5 - Final)

Назначение:
- собирает полный execution context
- объединяет:
    task + knowledge + routing
- передаёт это дальше в Executor

ВАЖНО:
- НЕ строит prompt
- НЕ вызывает модель
- только сбор контекста

Архитектура:
Task → ContextBuilder → Executor
"""

from kernel.knowledge.knowledge_builder import KnowledgeBuilder
from kernel.execution.model_router import ModelRouter


class ContextBuilder:
    def __init__(self):
        """
        Инициализация зависимостей
        """

        # Knowledge слой (RAG)
        self.knowledge_builder = KnowledgeBuilder()

        # Router (выбор модели)
        self.model_router = ModelRouter()

    # --------------------------------------------------
    # MAIN METHOD
    # --------------------------------------------------
    def build(self, task) -> dict:
        """
        Собирает полный context

        :param task: объект задачи
        :return: dict context
        """

        # -------------------------
        # 1. Базовый context
        # -------------------------
        context = {
            "task_id": task.id,
            "input": task.input_data,
            "task_type": "simple"  # пока фиксированный (потом можно расширить)
        }

        print("\n🧱 BASE CONTEXT:")
        print(context)

        # -------------------------
        # 2. Knowledge (RAG)
        # -------------------------
        knowledge = self.knowledge_builder.build(task.input_data)

        context["knowledge"] = knowledge

        print("\n📚 CONTEXT WITH KNOWLEDGE:")
        print(context["knowledge"])

        # -------------------------
        # 3. Routing (модель)
        # -------------------------
        route = self.model_router.route(context)

        context["execution_type"] = route.get("type")
        context["model"] = route.get("model")

        print("\n🧠 ROUTING DECISION:")
        print(route)

        # -------------------------
        # 4. Финальный context
        # -------------------------
        print("\n📦 FINAL CONTEXT:")
        for key, value in context.items():
            print(f"{key}: {value}")

        return context