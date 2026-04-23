"""
Qdrant Storage Client (Production Ready)

Responsibilities:
- connect to Qdrant
- insert/update vectors (upsert)
- perform semantic search

IMPORTANT:
- Uses NEW Qdrant API (query_points)
- Designed for scalability and future extensions
"""

from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


class QdrantStorage:
    """
    Qdrant storage wrapper.

    This class abstracts all interactions with Qdrant.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection: str = "content_v1"
    ):
        """
        Initialize Qdrant client.

        Args:
            host (str): Qdrant host
            port (int): Qdrant port
            collection (str): collection name
        """

        self.client = QdrantClient(host=host, port=port)
        self.collection = collection

    # ------------------------------------------------------------------
    # UPSERT (insert or update vectors)
    # ------------------------------------------------------------------
    def upsert(
        self,
        ids: List[str],
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]]
    ) -> None:
        """
        Insert or update vectors in Qdrant.

        Args:
            ids (List[str]): unique IDs for vectors
            vectors (List[List[float]]): embeddings
            payloads (List[dict]): metadata

        IMPORTANT:
        - ids must be unique (UUID recommended)
        - vectors must match collection vector size
        """

        if not (len(ids) == len(vectors) == len(payloads)):
            raise ValueError("IDs, vectors and payloads must have same length")

        points = []

        for i in range(len(ids)):
            points.append(
                PointStruct(
                    id=ids[i],
                    vector=vectors[i],
                    payload=payloads[i]
                )
            )

        # Upsert to Qdrant
        self.client.upsert(
            collection_name=self.collection,
            points=points
        )

    # ------------------------------------------------------------------
    # SEARCH (semantic search)
    # ------------------------------------------------------------------
    def search(
        self,
        query_vector: List[float],
        limit: int = 3
    ):
        """
        Perform semantic search.

        Args:
            query_vector (List[float]): query embedding
            limit (int): number of results

        Returns:
            List of results with:
                - score
                - payload
        """

        results = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            limit=limit
        )

        return results.points

    # ------------------------------------------------------------------
    # HEALTH CHECK (optional but useful)
    # ------------------------------------------------------------------
    def health_check(self) -> bool:
        """
        Check if Qdrant is available.

        Returns:
            bool
        """

        try:
            self.client.get_collections()
            return True
        except Exception:
            return False