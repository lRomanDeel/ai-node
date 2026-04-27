"""
End-to-End Ingestion Test (Production-style)

Pipeline:
Loader → Cleaner → Chunker → PostgreSQL → Embedder → Qdrant → Search

This script validates the full ingestion + storage + retrieval flow.
"""

import uuid

from kernel.ingestion.loaders.file_loader import FileLoader
from kernel.ingestion.cleaners.text_cleaner import TextCleaner
from kernel.ingestion.chunkers.text_chunker import TextChunker
from kernel.ingestion.embedders.local_embedder import LocalEmbedder

from kernel.storage.qdrant_client import QdrantStorage
from kernel.storage.postgres_client import PostgresStorage


def main():
    # ---------------------------------------------------------
    # INIT COMPONENTS
    # ---------------------------------------------------------
    loader = FileLoader()
    cleaner = TextCleaner()
    chunker = TextChunker()
    embedder = LocalEmbedder()

    qdrant = QdrantStorage()
    postgres = PostgresStorage()

    print("🚀 Starting ingestion pipeline...")

    # ---------------------------------------------------------
    # LOAD DOCUMENT
    # ---------------------------------------------------------
    doc = loader.load("data/test.md")
    print("📄 Loaded document")

    # ---------------------------------------------------------
    # CLEAN TEXT
    # ---------------------------------------------------------
    cleaned_text = cleaner.clean(doc["content"])
    print("🧹 Cleaned text")

    # ---------------------------------------------------------
    # CHUNK TEXT
    # ---------------------------------------------------------
    chunks = chunker.chunk(cleaned_text)
    print(f"✂️ Created {len(chunks)} chunks")

    # ---------------------------------------------------------
    # SAVE DOCUMENT TO POSTGRES
    # ---------------------------------------------------------
    doc_id = postgres.create_document(
        source="test.md",
        content=doc["content"]
    )
    print(f"🗂 Document saved to Postgres: {doc_id}")

    # ---------------------------------------------------------
    # SAVE CHUNKS TO POSTGRES
    # ---------------------------------------------------------
    chunk_ids = postgres.create_chunks(doc_id, chunks)
    print(f"🧩 {len(chunk_ids)} chunks saved to Postgres")

    # ---------------------------------------------------------
    # GENERATE EMBEDDINGS
    # ---------------------------------------------------------
    embeddings = embedder.embed(chunks)
    print(f"🧠 Generated embeddings (size={len(embeddings[0])})")

    # ---------------------------------------------------------
    # PREPARE QDRANT DATA
    # ---------------------------------------------------------
    payloads = []

    for i, chunk in enumerate(chunks):
        payloads.append({
            "text": chunk,
            "chunk_index": i,
            "document_id": doc_id,        # 🔥 связь с PostgreSQL
            "chunk_id": chunk_ids[i],     # 🔥 связь с PostgreSQL
            "source": "test.md",
            "type": "article",
            "embedding_model": embedder.get_model_name()
        })

    # ---------------------------------------------------------
    # SAVE TO QDRANT
    # ---------------------------------------------------------
    qdrant.upsert(chunk_ids, embeddings, payloads)
    print("✅ Saved embeddings to Qdrant")

    # ---------------------------------------------------------
    # SEARCH TEST
    # ---------------------------------------------------------
    query = "test ingestion"
    print(f"\n🔍 Query: {query}")

    query_vector = embedder.embed([query])[0]
    results = qdrant.search(query_vector)

    print("\n📊 SEARCH RESULTS:")

    for i, r in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print("Score:", r.score)
        print("Text:", r.payload.get("text"))
        print("Document ID:", r.payload.get("document_id"))
        print("Chunk ID:", r.payload.get("chunk_id"))


if __name__ == "__main__":
    main()