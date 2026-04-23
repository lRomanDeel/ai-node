Ingestion Pipeline — Production Specification
1. Overview

Ingestion Pipeline is responsible for:

 - processing raw data sources
 - transforming them into structured knowledge
 - generating embeddings
 - storing data in system storage

2. Architecture
Input → Loader → Cleaner → Chunker → Embedder → Storage → Validation

3. Components
  3.1 Loader

Loads input data:
.txt
.md

  3.2 Cleaner
removes noise
normalizes text
strips HTML

  3.3 Chunker
splits text into semantic chunks
preserves context using overlap

Parameters:

chunk_size: 600 tokens
overlap: 120 tokens

  3.4 Embedder

Model:

bge-small-en-v1.5 (local)

Rules:

single model for entire system
embeddings must be consistent

  3.5 Storage
Vector storage → Qdrant
Metadata → PostgreSQL
Files → MinIO 


  3.6 Validation Layer

Ensures:

chunk quality
no duplicates
valid embeddings


4. Data Flow
 Load file
 Calculate hash
 Check duplication
 Clean text
 Chunk text
 Validate chunks
 Generate embeddings
 Store data
 Log results


5. Idempotency

Each document identified by:

sha256(file_content)

If exists → skip


6. Logging

Pipeline logs:

start / end
errors
chunk count
processing time


7. Validation Rules

Reject chunk if:

too small
duplicate
low quality


8. Performance Requirements
processing time < 2 sec / doc (small files)
embedding batching supported


9. Failure Handling
retry embedding
skip broken documents
log all failures

10. Scalability Strategy

Future:

async pipeline
queue-based processing
distributed workers
