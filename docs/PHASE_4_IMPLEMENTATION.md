# Phase 4 Implementation: Evidence Retrieval / RAG

## Objective
Transform CIRAN's legacy Python/BFS in-memory traversal for the Copilot into a robust, trace-preserving Retrieval-Augmented Generation (RAG) architecture using PostgreSQL, `pgvector`, and Neo4j.

## Architecture

1. **Embedding**: `text-embedding-3-small` (1536 dimensions) via OpenAI.
2. **Chunking**: Deterministic chunking (500 characters, 50-character overlap) mapped back to the source `RawRecord`.
3. **Storage**: PostgreSQL `document_chunks` table utilizing `pgvector` for scalable, similarity-based vector search.
4. **Graph Context**: Retrieved document vectors provide exact `record_id`s, which are dynamically used to retrieve Neo4j relationships originating from those source records (graph-aware context).
5. **LLM Generation**: Instructs the model to draw strictly from the provided Document Evidence and Graph Evidence without fabricating IDs or relationships.

## Key Changes

### 1. Vector Setup
- **Dependencies**: Added `pgvector>=0.2.1` to `requirements.txt`.
- **Database Extension**: Enabled `CREATE EXTENSION IF NOT EXISTS vector` in `db.py`.
- **Models**: Introduced `DocumentChunk` in `sql_models.py` with `Vector(1536)` mapping to `RawRecord.id`.

### 2. Ingestion Pipeline
- Augmented `IngestionService` to tokenize parsed document text using `ChunkingService`.
- Embedded chunks synchronously via `EmbeddingService`.
- Protected ingestion flow: If embeddings fail (e.g., API limits), the record gracefully defaults to a degraded but successful state without losing the core parsed text.

### 3. ContextBuilder & Vector Search
- `VectorSearchService` safely bounds requests with a `top_k=20` ceiling using cosine distance `<=>`.
- `ContextBuilder` resolves document chunks into graph evidence. It strictly enforces provenance: a relationship is only added to context if its `sourceRecord` matches a retrieved `record_id`.

### 4. Copilot Detachment from state.py
- Refactored `CopilotRetrievalService` and `copilot.py` to decouple from `state.py` entirely, utilizing SQLAlchemy Database sessions and Neo4j driver sessions.

## State Dependencies Documentation
The legacy `CorrelationEngine` currently maintains a dependency on `state.py` (via `RelationshipEngine`). Since its focus is deep cross-case logical permutations rather than pure semantic QA, a full rewrite was excluded from Phase 4 scope to minimize instability.

## Runtime Verification
**IMPLEMENTATION STATUS**: Completed according to architecture standards.
**RUNTIME VERIFICATION STATUS**: Blocked locally due to missing Docker services for Neo4j and PostgreSQL `pgvector`. Verification relies on `pytest` logical boundaries and structural mapping.
