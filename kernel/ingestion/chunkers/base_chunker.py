"""
Base Chunker Interface
"""

from abc import ABC, abstractmethod
from typing import List


class BaseChunker(ABC):
    """
    Abstract chunker interface.
    """

    @abstractmethod
    def chunk(self, text: str) -> List[str]:
        """
        Split text into chunks.

        Args:
            text (str)

        Returns:
            List[str]
        """
        pass
