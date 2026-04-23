"""
Base Loader Interface

Defines a unified interface for all data loaders.
This allows us to easily extend ingestion sources in future:
- files
- APIs
- telegram
- web scraping

IMPORTANT:
We keep this abstraction to later extract ingestion into a separate service
without refactoring the core logic.
"""

from abc import ABC, abstractmethod
from typing import Dict


class BaseLoader(ABC):
    """
    Abstract base class for all loaders.

    Each loader must implement the load() method
    and return normalized document format.
    """

    @abstractmethod
    def load(self, source: str) -> Dict:
        """
        Load data from source and return normalized document.

        Args:
            source (str): path or identifier of the data source

        Returns:
            Dict:
            {
                "content": str,
                "metadata": {
                    "source": str,
                    "format": str,
                    "language": str
                }
            }
        """
        pass
