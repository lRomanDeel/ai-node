"""
Qdrant Client (Stage 5 - Fixed)

Использует НОВЫЙ API Qdrant
"""

from qdrant_client import QdrantClient


class QdrantClientWrapper:
    def __init__(self):
        self.client = QdrantClient(
            host="localhost",
            port=6333
        )

    # --------------------------------------------------
    def search(self, collection_name: str, query_vector: list, limit: int = 5):
        """
        Новый способ поиска через query_points
        """

        try:
            results = self.client.query_points(
                collection_name=collection_name,
                query=query_vector,
                limit=limit
            )

            # ВАЖНО: теперь points лежат внутри
            return results.points

        except Exception as e:
            print(f"\n❌ Qdrant search error: {e}")
            return []