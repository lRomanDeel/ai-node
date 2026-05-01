"""
Full Pipeline Test (Stage 5)

Назначение:
- проверить полный цикл:
  Task → Context → Knowledge (RAG) → Prompt → Execution → Response

Проверяем:
✔ работает ли RAG
✔ попадает ли knowledge в prompt
✔ использует ли модель контекст
✔ fallback поведение (если нет данных)
"""

from kernel.context.context_builder import ContextBuilder
from kernel.execution.executor import Executor


# --------------------------------------------------
# MOCK TASK (упрощённая модель задачи)
# --------------------------------------------------
class DummyTask:
    def __init__(self, task_id: str, input_text: str):
        self.id = task_id
        self.input_data = input_text


# --------------------------------------------------
# MAIN TEST
# --------------------------------------------------
def run_test(input_text: str):
    print("\n🚀 FULL PIPELINE START\n")

    # 1. Создаём задачу
    task = DummyTask("task-001", input_text)

    # 2. Context Builder
    context_builder = ContextBuilder()
    context = context_builder.build(task)

    # 3. Лог контекста
    print("\n📦 CONTEXT:\n")
    for key, value in context.items():
        print(f"{key}: {value}\n")

    # 4. Executor
    executor = Executor()

    print("\n🤖 GENERATING RESPONSE...\n")

    response = executor.execute(context)

    # 5. Финальный ответ
    print("\n\n✅ FINAL RESPONSE:\n")
    print(response)


# --------------------------------------------------
# ТЕСТОВЫЕ СЦЕНАРИИ
# --------------------------------------------------
if __name__ == "__main__":

    # ==========================================
    # ТЕСТ 1 — RAG ДОЛЖЕН СРАБОТАТЬ
    # ==========================================
    print("\n==============================")
    print("TEST 1: RAG SHOULD BE USED")
    print("==============================")

    run_test("What is the test document about?")

    # ==========================================
    # ТЕСТ 2 — НЕТ RAG (должен сказать не знаю)
    # ==========================================
    print("\n==============================")
    print("TEST 2: NO CONTEXT FALLBACK")
    print("==============================")

    run_test("What is quantum teleportation?")