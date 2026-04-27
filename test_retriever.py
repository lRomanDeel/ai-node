from kernel.context.retriever import Retriever

retriever = Retriever()

results = retriever.search("test ingestion")

print("\nRETRIEVER RESULTS:\n")

for r in results:
    print("Score:", r["score"])
    print("Text:", r["text"])
    print("Document:", r["document_id"])
    print("Chunk:", r["chunk_id"])
    print("-" * 40)
