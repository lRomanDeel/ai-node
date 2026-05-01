"""
Retriever (Stage 5 - Final, FIXED)

Назначение:
- выполняет поиск по векторной базе (Qdrant)
- возвращает релевантные документы

ВАЖНО:
- использует НОВЫЙ API Qdrant (query_points)
- НЕ знает про prompt / execution
- только retrieval слой

Архитектура:
Query → Embedding → Qdrant → Results
"""

from sentence_transformers import SentenceTransformer
from kernel.storage.qdrant_client import QdrantClientWrapper


class Retriever:
    def __init__(self):
        """
        Инициализация Retriever

        Здесь:
        - подключаем embedding модель
        - подключаем Qdrant client
        """

        # 🔥 ВАЖНО: должна совпадать с ingestion
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # клиент Qdrant (наш wrapper)
        self.client = QdrantClientWrapper()

        # имя коллекции
        self.collection_name = "content_v1"

    # --------------------------------------------------
    # MAIN SEARCH METHOD
    # --------------------------------------------------
    def search(self, query: str, limit: int = 5) -> list:
        """
        Выполняет поиск по векторной БД

        :param query: текст запроса
        :param limit: сколько результатов вернуть
        :return: список результатов (dict)
        """

        if not query:
            return []

        print("\n🔎 QUERY:", query)

        # -------------------------
        # 1. Генерация embedding
        # -------------------------
        query_vector = self.model.encode(query).tolist()

        # -------------------------
        # 2. Поиск в Qdrant (НОВЫЙ API)
        # -------------------------
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )

        print("\n📦 RAW QDRANT RESULTS:")
        print(results)

        # -------------------------
        # 3. Приводим к нормальному формату
        # -------------------------
        formatted_results = []

        for r in results:
            try:
                formatted_results.append({
                    "payload": r.payload,   # текст документа
                    "score": r.score        # релевантность
                })
            except Exception:
                continue

        print("\n✅ FORMATTED RESULTS:")
        print(formatted_results)

        return formatted_results