"""
Retriever Module

Responsibilities:
- search in Qdrant
- fetch chunk data from PostgreSQL
"""

from typing import List

from kernel.storage.qdrant_client import QdrantStorage
from kernel.storage.postgres_client import PostgresStorage
from kernel.ingestion.embedders.local_embedder import LocalEmbedder


class Retriever:
    """
    Core retrieval logic
    """

    def __init__(self):
        self.qdrant = QdrantStorage()
        self.postgres = PostgresStorage()
        self.embedder = LocalEmbedder()

    def search(self, query: str, limit: int = 3) -> List[dict]:
        """
        Perform semantic search and return enriched results
        """

        # 🔍 convert query → embedding
        query_vector = self.embedder.embed([query])[0]

        # 🔍 search in Qdrant
        results = self.qdrant.search(query_vector, limit=limit)

        enriched_results = []

        for r in results:
            payload = r.payload

            chunk_id = payload.get("chunk_id")
            document_id = payload.get("document_id")

            # 🔥 достаём текст из Postgres
            chunk_text = self.get_chunk_text(chunk_id)

            enriched_results.append({
                "score": r.score,
                "chunk_id": chunk_id,
                "document_id": document_id,
                "text": chunk_text
            })

        return enriched_results

    def get_chunk_text(self, chunk_id: str) -> str:
        """
        Fetch chunk text from PostgreSQL
        """

        with self.postgres.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT text FROM chunks WHERE id = %s
                """,
                (chunk_id,)
            )

            result = cursor.fetchone()

            if result:
                return result[0]

        return ""
