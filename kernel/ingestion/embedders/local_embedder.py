"""
Local Embedder (Production Ready)

Uses sentence-transformers.
"""

from typing import List
from sentence_transformers import SentenceTransformer

from .base_embedder import BaseEmbedder


class LocalEmbedder(BaseEmbedder):
    """
    Local embedding implementation.
    """

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5", batch_size: int = 32):
        self.model_name = model_name
        self.batch_size = batch_size

        # Load model once
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=True
        )

        return embeddings.tolist()

    def get_model_name(self) -> str:
        return self.model_name

