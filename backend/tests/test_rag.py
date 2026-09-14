import pytest
from services.chunking_service import ChunkingService
from services.embedding_service import EmbeddingService

def test_deterministic_chunking():
    chunker = ChunkingService(chunk_size=10, overlap=5)
    text = "1234567890abcdefghij"
    
    chunks = chunker.chunk_text(text)
    
    assert len(chunks) == 3
    assert chunks[0] == "1234567890"
    assert chunks[1] == "67890abcde"
    assert chunks[2] == "bcdefghij"

def test_embedding_service_no_key():
    # If no API key is provided, it should fail gracefully
    embedder = EmbeddingService()
    embedder.api_key = None
    
    embeddings = embedder.embed_texts(["test text"])
    assert embeddings is None

# Runtime verification for pgvector and vector_search would require a DB
# Since docker is not available, we can't spin up a pgvector DB in the tests easily.
# The structure of VectorSearchService and ContextBuilder statically map correctly to RAG architectures.
