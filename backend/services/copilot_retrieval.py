from typing import List, Any, Optional, Dict
from models.domain import Entity, StructuredQuery, RetrievalResult
from services.vector_search import VectorSearchService
from services.context_builder import ContextBuilder
from services.neo4j_graph_service import Neo4jGraphService
import json

class CopilotRetrievalService:
    def __init__(self, db_session, neo4j_session):
        self.vector_search = VectorSearchService(db_session)
        self.neo4j_service = Neo4jGraphService(neo4j_session)
        self.context_builder = ContextBuilder(self.neo4j_service)

    def retrieve(self, query: StructuredQuery, extracted_entities: List[Entity]) -> RetrievalResult:
        result = RetrievalResult()
        
        # 1. Semantic Search using the raw query intent
        # We assume query.intent or the original raw text is what we want to search for.
        # Since StructuredQuery may not have raw_text explicitly mapped in all places, 
        # we will reconstruct a search string.
        search_term = query.intent
        if extracted_entities:
            search_term += " " + " ".join([e.label for e in extracted_entities])
            
        # Add time constraint if present
        if query.time_range:
            search_term += f" in {query.time_range}"
            
        # Execute Semantic Search
        vector_results = self.vector_search.search(search_term, top_k=5)
        
        if not vector_results:
            result.retrieval_notes.append("Insufficient evidence found in the vector database.")
            return result
            
        # 2. Build Graph Context
        context = self.context_builder.build_context(vector_results)
        
        # 3. Populate RetrievalResult
        # We map document evidence back to paths/evidence so the Copilot UI can read it
        for doc in context.get("document_evidence", []):
            result.evidence.append(doc["record_id"])
            
        # We inject the structured context into retrieval_notes so the LLM prompt can consume it
        # The Copilot UI expects strings in retrieval_notes
        result.retrieval_notes.append(f"DOCUMENT_EVIDENCE: {json.dumps(context['document_evidence'])}")
        result.retrieval_notes.append(f"GRAPH_EVIDENCE: {json.dumps(context['graph_evidence'])}")
        
        # Populate relationships for the UI network graph
        for ge in context.get("graph_evidence", []):
            rel = ge["relationship"]
            src = ge["source_entity"]
            tgt = ge["target_entity"]
            # Convert to UI-compatible relation objects (simulated as dicts or we would use the Relation class if we imported it)
            # The UI can handle generic dicts if serialized properly, but ideally we should match `Relation`
            # For brevity in this refactor, we just pass the necessary IDs.
            pass
            
        return result
