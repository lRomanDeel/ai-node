"""
Retriever Test (Stage 5)

Назначение:
- проверить работу retrieval слоя отдельно
- убедиться что:
    ✔ Qdrant содержит данные
    ✔ embedding работает
    ✔ поиск возвращает результат

ВАЖНО:
- это unit-тест retrieval
- без context / prompt / executor
"""

from kernel.context.retriever import Retriever


def run_test():
    print("\n🚀 RETRIEVER TEST START\n")

    # -------------------------
    # 1. Инициализация
    # -------------------------
    retriever = Retriever()

    # -------------------------
    # 2. Тестовый запрос
    # -------------------------
    query = "test document"

    print(f"\n🔎 QUERY: {query}")

    # -------------------------
    # 3. Поиск
    # -------------------------
    results = retriever.search(query)

    # -------------------------
    # 4. Вывод результатов
    # -------------------------
    print("\n📦 FINAL RESULTS:\n")

    if not results:
        print("❌ NO RESULTS FOUND")
        return

    for i, r in enumerate(results, 1):
        payload = r.get("payload", {})
        text = payload.get("text", "")
        score = r.get("score", 0)

        print(f"\n--- RESULT #{i} ---")
        print(f"Score: {score}")
        print(f"Text: {text}")

    print("\n✅ RETRIEVER WORKS\n")


# --------------------------------------------------
# RUN
# --------------------------------------------------
if __name__ == "__main__":
    run_test()