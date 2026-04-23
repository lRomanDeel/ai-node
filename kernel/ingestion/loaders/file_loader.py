"""
File Loader Implementation

Supports:
- .txt
- .md

Responsibilities:
- read file
- validate format
- return normalized document

IMPORTANT:
- No cleaning here (done in Cleaner)
- No chunking here
- Only loading raw content
"""

import os
from typing import Dict

from .base_loader import BaseLoader


class FileLoader(BaseLoader):
    """
    Loader for local text-based files.

    Supported formats:
    - .txt
    - .md
    """

    SUPPORTED_EXTENSIONS = [".txt", ".md"]

    def load(self, source: str) -> Dict:
        """
        Load file and return normalized document.

        Args:
            source (str): file path

        Returns:
            Dict: normalized document

        Raises:
            FileNotFoundError
            ValueError (unsupported format)
        """

        # --- 1. Validate file existence ---
        if not os.path.exists(source):
            raise FileNotFoundError(f"File not found: {source}")

        # --- 2. Validate extension ---
        _, ext = os.path.splitext(source)

        if ext.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file format: {ext}")

        # --- 3. Read file content ---
        try:
            with open(source, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            raise RuntimeError(f"Failed to read file: {e}")

        # --- 4. Minimal validation ---
        if not content.strip():
            raise ValueError("File is empty")

        # --- 5. Return normalized document ---
        return {
            "content": content,
            "metadata": {
                "source": "file",
                "format": ext.replace(".", ""),
                "language": "unknown"  # will be detected later if needed
            }
        }
