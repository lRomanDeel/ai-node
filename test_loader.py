"""
End-to-End Ingestion + Qdrant Test

Pipeline:
Loader → Cleaner → Chunker → Embedder → Qdrant → Search

This is a production-style test script.
"""

import uuid

from kernel.ingestion.loaders.file_loader import FileLoader
from kernel.ingestion.cleaners.text_cleaner import TextCleaner
from kernel.ingestion.chunkers.text_chunker import TextChunker
from kernel.ingestion.embedders.local_embedder import LocalEmbedder
from kernel.storage.qdrant_client import QdrantStorage


def main():
    # --- init components ---
    loader = FileLoader()
    cleaner = TextCleaner()
    chunker = TextChunker()
    embedder = LocalEmbedder()
    storage = QdrantStorage()

    print("🚀 Starting ingestion pipeline...")

    # --- load document ---
    doc = loader.load("data/test.md")
    print("📄 Loaded document")

    # --- clean text ---
    cleaned_text = cleaner.clean(doc["content"])
    print("🧹 Cleaned text")

    # --- chunk ---
    chunks = chunker.chunk(cleaned_text)
    print(f"✂️ Created {len(chunks)} chunks")

    # --- embed ---
    embeddings = embedder.embed(chunks)
    print(f"🧠 Generated embeddings (size={len(embeddings[0])})")

    # --- prepare data for Qdrant ---
    ids = [str(uuid.uuid4()) for _ in chunks]

    payloads = []
    for i, chunk in enumerate(chunks):
        payloads.append({
            "text": chunk,
            "chunk_index": i,
            "source": "test.md",
            "type": "article",
            "embedding_model": embedder.get_model_name()
        })

    # --- save to Qdrant ---
    storage.upsert(ids, embeddings, payloads)
    print("✅ Saved to Qdrant")

    # --- search test ---
    query = "test ingestion"
    print(f"\n🔍 Query: {query}")

    query_vector = embedder.embed([query])[0]
    results = storage.search(query_vector)

    print("\n📊 SEARCH RESULTS:")
    for i, r in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print("Score:", r.score)
        print("Text:", r.payload.get("text"))


if __name__ == "__main__":
    main()
