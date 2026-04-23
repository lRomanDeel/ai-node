"""
Text Chunker (Production Ready)

Key features:
- chunk size control
- overlap support
- sentence-aware splitting

IMPORTANT:
Chunking quality directly affects RAG performance.
"""

from typing import List


class TextChunker:
    """
    Production-ready chunker.
    """

    def __init__(self, chunk_size: int = 600, overlap: int = 120):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        """
        Split text into chunks with overlap.

        Strategy:
        - split by sentences
        - build chunks up to chunk_size
        - apply overlap
        """

        # --- 1. Split into sentences ---
        sentences = text.split(". ")

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()

            if not sentence:
                continue

            # add dot back (lost in split)
            sentence = sentence + "."

            # --- 2. Check size ---
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += " " + sentence
            else:
                chunks.append(current_chunk.strip())

                # --- 3. Apply overlap ---
                overlap_text = current_chunk[-self.overlap:]

                current_chunk = overlap_text + " " + sentence

        # --- 4. Add last chunk ---
        if current_chunk:
            chunks.append(current_chunk.strip())

        # --- 5. Validation ---
        chunks = [c for c in chunks if len(c) > 50]

        return chunks
