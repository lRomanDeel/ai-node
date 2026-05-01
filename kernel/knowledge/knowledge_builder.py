"""
Knowledge Builder (Stage 5 - Final)

Назначение:
- собирает знания из retrieval слоя (Qdrant)
- нормализует данные
- фильтрует мусор
- возвращает структурированный knowledge

ВАЖНО:
- НЕ знает про prompt
- НЕ знает про execution
- только подготовка знаний

Архитектура:
Retriever → KnowledgeBuilder → ContextBuilder
"""

from kernel.context.retriever import Retriever


class KnowledgeBuilder:
    def __init__(self):
        """
        Инициализация KnowledgeBuilder
        """
        self.retriever = Retriever()

    # --------------------------------------------------
    # MAIN METHOD
    # --------------------------------------------------
    def build(self, input_text: str) -> dict:
        """
        Собирает knowledge для context

        :param input_text: текст запроса
        :return: dict knowledge
        """

        # -------------------------
        # 1. Получаем данные из Retriever
        # -------------------------
        results = self.retriever.search(input_text) or []

        print("\n📄 RAW RETRIEVER DATA:")
        print(results)

        documents = []

        # -------------------------
        # 2. Обрабатываем результаты
        # -------------------------
        for r in results:
            payload = r.get("payload", {})
            text = payload.get("text", "")
            score = r.get("score", 0)

            # ❗ фильтр пустых документов
            if not text:
                continue

            # ❗ фильтр по релевантности (очень важно)
            if score < 0.1:
                continue

            documents.append({
                "text": text.strip(),
                "score": score
            })

        # -------------------------
        # 3. Ограничение количества
        # -------------------------
        documents = documents[:5]

        # -------------------------
        # 4. Финальный knowledge
        # -------------------------
        knowledge = {
            "documents": documents,
            "metadata": {
                "source": "qdrant",
                "count": len(documents)
            }
        }

        print("\n📚 FINAL KNOWLEDGE:")
        print(knowledge)

        return knowledge