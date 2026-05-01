"""
Executor (Stage 5 - FINAL, PRODUCTION READY)

Назначение:
- принимает готовый context
- валидирует наличие RAG (knowledge)
- строит prompt
- вызывает LLM
- возвращает результат

ВАЖНО:
- НЕ содержит логики retrieval
- НЕ содержит логики выбора модели
- работает только с готовым context

Архитектура:
Context → Executor → LLM → Response

КЛЮЧЕВОЕ:
- реализован HARD GUARDRAIL (RAG enforcement)
"""

from kernel.prompt.prompt_builder import PromptBuilder
from kernel.llm.ollama_client import OllamaClient


class Executor:
    def __init__(self):
        """
        Инициализация зависимостей
        """
        self.prompt_builder = PromptBuilder()
        self.client = OllamaClient()

    # --------------------------------------------------
    # MAIN ENTRY POINT
    # --------------------------------------------------
    def execute(self, context: dict) -> str:
        """
        Выполнение задачи

        :param context: execution context
        :return: текст ответа модели
        """

        print("\n🤖 GENERATING RESPONSE...\n")

        # -------------------------
        # 1. ЛОГ КОНТЕКСТА
        # -------------------------
        print("📦 FULL CONTEXT:")
        for key, value in context.items():
            print(f"{key}: {value}")

        # -------------------------
        # 2. ПРОВЕРКА KNOWLEDGE (🔥 HARD GUARDRAIL)
        # -------------------------
        knowledge = context.get("knowledge", {})
        documents = knowledge.get("documents", [])

        print("\n📚 KNOWLEDGE USED:")
        print(knowledge)

        # ❗ КРИТИЧЕСКИЙ МОМЕНТ
        if not documents:
            print("\n⛔ RAG BLOCK: no documents found")
            return "I don't know based on the provided context."

        # -------------------------
        # 3. СТРОИМ PROMPT
        # -------------------------
        prompt = self.prompt_builder.build(context)

        print("\n🧠 PROMPT:")
        print(prompt)

        # -------------------------
        # 4. ВЫБОР МОДЕЛИ
        # -------------------------
        model = context.get("model", "tinyllama")

        print(f"\n🧠 Using model: {model}")
        print("\n💬 Streaming response:\n")

        # -------------------------
        # 5. ВЫЗОВ МОДЕЛИ
        # -------------------------
        try:
            response = self.client.generate(
                model=model,
                prompt=prompt
            )

            # -------------------------
            # 6. ВОЗВРАТ РЕЗУЛЬТАТА
            # -------------------------
            return response

        except Exception as e:
            print(f"\n❌ Execution error: {e}")
            return "❌ Execution failed"