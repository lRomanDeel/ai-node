"""
Base Cleaner Interface

Responsible for text normalization before chunking.
"""

from abc import ABC, abstractmethod


class BaseCleaner(ABC):
    """
    Abstract cleaner interface.
    """

    @abstractmethod
    def clean(self, text: str) -> str:
        """
        Clean and normalize text.

        Args:
            text (str): raw input text

        Returns:
            str: cleaned text
        """
        pass
