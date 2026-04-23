"""
Base Embedder Interface

Defines abstraction layer for embeddings.

IMPORTANT:
Allows easy model switching in future.
"""

from abc import ABC, abstractmethod
from typing import List


class BaseEmbedder(ABC):
    """
    Abstract embedding interface.
    """

    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings.

        Args:
            texts (List[str])

        Returns:
            List[List[float]]
        """
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """
        Return embedding model name.
        """
        pass
