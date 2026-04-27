"""
Context Builder Module

Responsibilities:
- retrieve relevant chunks
- assemble them into a structured context
- prepare data for LLM input

This is a core part of the RAG pipeline.
"""

from typing import List, Dict

from kernel.context.retriever import Retriever


class ContextBuilder:
    """
    Builds context from retrieved chunks
    """

    def __init__(self):
        """
        Initialize retriever
        """
        self.retriever = Retriever()

    # ------------------------------------------------------------------
    # BUILD CONTEXT
    # ------------------------------------------------------------------
    def build(self, query: str, limit: int = 3) -> str:
        """
        Build plain text context for LLM

        :param query: user query
        :param limit: number of chunks to retrieve
        :return: formatted context string
        """

        # 🔍 Step 1: retrieve relevant chunks
        results = self.retriever.search(query, limit=limit)

        if not results:
            return ""

        # 🧩 Step 2: extract text blocks
        context_blocks = []

        for r in results:
            text = r.get("text", "").strip()

            if text:
                context_blocks.append(text)

        # 🧠 Step 3: join into final context
        context = "\n\n".join(context_blocks)

        return context

    # ------------------------------------------------------------------
    # BUILD STRUCTURED CONTEXT (ADVANCED / FUTURE USE)
    # ------------------------------------------------------------------
    def build_structured(self, query: str, limit: int = 3) -> List[Dict]:
        """
        Build structured context (for advanced usage / debugging / ranking)

        :return: list of chunk dicts
        """

        results = self.retriever.search(query, limit=limit)

        structured = []

        for r in results:
            structured.append({
                "score": r.get("score"),
                "text": r.get("text"),
                "document_id": r.get("document_id"),
                "chunk_id": r.get("chunk_id")
            })

        return structured

    # ------------------------------------------------------------------
    # BUILD CONTEXT WITH METADATA (OPTIONAL)
    # ------------------------------------------------------------------
    def build_with_metadata(self, query: str, limit: int = 3) -> str:
        """
        Build context including metadata (debug / trace mode)

        :return: formatted string with metadata
        """

        results = self.retriever.search(query, limit=limit)

        blocks = []

        for i, r in enumerate(results):
            block = (
                f"[Chunk {i+1}]\n"
                f"Score: {r.get('score')}\n"
                f"Document: {r.get('document_id')}\n"
                f"Chunk: {r.get('chunk_id')}\n"
                f"Text:\n{r.get('text')}"
            )

            blocks.append(block)

        return "\n\n---\n\n".join(blocks)
