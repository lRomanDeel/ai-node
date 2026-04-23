"""
Text Cleaner (Production Ready)

Responsibilities:
- normalize whitespace
- remove unwanted patterns
- basic noise filtering

IMPORTANT:
Cleaner must NOT destroy semantic meaning.
"""

import re
from .base_cleaner import BaseCleaner


class TextCleaner(BaseCleaner):
    """
    Production-ready text cleaner.
    """

    def clean(self, text: str) -> str:
        """
        Clean input text.

        Steps:
        1. Remove excessive whitespace
        2. Remove common noise patterns
        3. Normalize line breaks
        """

        # --- 1. Normalize whitespace ---
        text = re.sub(r'\s+', ' ', text)

        # --- 2. Normalize line breaks ---
        text = text.replace(" .", ".")
        text = text.replace(" ,", ",")

        # --- 3. Remove common garbage patterns ---
        noise_patterns = [
            r"© \d{4}",
            r"All rights reserved",
            r"Subscribe now",
            r"Click here",
        ]

        for pattern in noise_patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        # --- 4. Trim ---
        text = text.strip()

        # --- 5. Minimal validation ---
        if len(text) < 20:
            raise ValueError("Text too short after cleaning")

        return text
