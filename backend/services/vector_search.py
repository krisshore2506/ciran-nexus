from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.sql_models import DocumentChunk
from services.embedding_service import EmbeddingService

class VectorSearchService:
    def __init__(self, db: Session):
        self.db = db
        self.embedder = EmbeddingService()

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Executes a semantic similarity search using pgvector cosine distance.
        Enforces a safe top_k maximum of 20.
        """
        if top_k > 20:
            top_k = 20
            
        # 1. Embed the query
        query_embedding_list = self.embedder.embed_texts([query])
        if not query_embedding_list or not query_embedding_list[0]:
            return []
            
        query_vector = query_embedding_list[0]
        
        # 2. Search database using cosine distance (<=>)
        # We order by distance, so lower is closer (higher similarity)
        stmt = (
            select(DocumentChunk)
            .order_by(DocumentChunk.embedding.cosine_distance(query_vector))
            .limit(top_k)
        )
        
        results = self.db.execute(stmt).scalars().all()
        
        # 3. Format output
        search_results = []
        for chunk in results:
            # Since pgvector doesn't directly return the distance in the ORM object easily 
            # without adding it to the select, we will just return the chunks.
            # We can compute similarity loosely, or just return them in ranked order.
            search_results.append({
                "chunk_id": chunk.id,
                "record_id": chunk.record_id,
                "text_content": chunk.text_content,
                "timestamp": chunk.timestamp,
                # Cosine similarity is roughly 1 - cosine_distance
                # We won't have the exact score unless we query for it, but we can return ranking order.
            })
            
        return search_results
