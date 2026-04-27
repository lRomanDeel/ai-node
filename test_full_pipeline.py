"""
FULL PIPELINE TEST

Task → Context → Execution → Response
"""

from kernel.context.context_builder import ContextBuilder
from kernel.execution.executor import Executor


class DummyTask:
    def __init__(self, input_text):
        self.id = "task-001"
        self.input_data = input_text


def main():
    print("\n🚀 FULL PIPELINE START\n")

    # 1. Context builder
    context_builder = ContextBuilder()

    # 2. Executor
    executor = Executor()

    # 3. ВАЖНО — длинный текст (включает RAG)
    task = DummyTask(
        "Explain how ingestion pipeline works in AI systems "
        "and how vector databases are used for semantic search"
    )

    # 4. Build context
    context = context_builder.build(task)

    print("\n📦 CONTEXT:\n")
    for k, v in context.items():
        print(f"{k}: {v}\n")

    # 5. Execute
    print("\n🤖 GENERATING RESPONSE...\n")

    response = executor.execute(context)

    print("\n✅ RESPONSE:\n")
    print(response)


if __name__ == "__main__":
    main()
