"""
Test: Execution Context + RAG Integration
"""

from kernel.context.context_builder import ContextBuilder


# -----------------------------
# Dummy Task (эмуляция системы)
# -----------------------------
class DummyTask:
    def __init__(self, input_text):
        self.id = "test-task-001"
        self.input_data = input_text


# -----------------------------
# TEST
# -----------------------------
def main():
    builder = ContextBuilder()

    # попробуй разные варианты
    task = DummyTask("processing text for AI system and vector embeddings")

    context = builder.build(task)

    print("\n========== FULL CONTEXT ==========\n")

    for key, value in context.items():
        print(f"{key}: {value}\n")


if __name__ == "__main__":
    main()
