from typing import List, Dict, Any
from services.neo4j_graph_service import Neo4jGraphService

class ContextBuilder:
    def __init__(self, neo4j_service: Neo4jGraphService):
        self.neo4j_service = neo4j_service

    def build_context(self, vector_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combines Vector Evidence with relevant Graph Context.
        Uses retrieved record_ids to find relationships in Neo4j mapped to those same records.
        """
        if not vector_results:
            return {
                "document_evidence": [],
                "graph_evidence": []
            }
            
        # Extract unique record IDs from the retrieved vector chunks
        record_ids = list(set([res["record_id"] for res in vector_results]))
        
        # 1. Document Evidence
        document_evidence = []
        for res in vector_results:
            document_evidence.append({
                "record_id": res["record_id"],
                "chunk_id": res["chunk_id"],
                "text": res["text_content"]
            })
            
        # 2. Graph Context
        graph_evidence = []
        
        # We query Neo4j for relationships that have a sourceRecord matching our retrieved records.
        # This guarantees we only pull graph context DIRECTLY supported by the retrieved documents.
        query = """
        MATCH (a)-[r]->(b)
        WHERE r.sourceRecord IN $record_ids
        RETURN a.id AS source_id, a.label AS source_label, labels(a) AS source_type,
               type(r) AS rel_type, r.confidence AS confidence, r.sourceRecord AS sourceRecord,
               b.id AS target_id, b.label AS target_label, labels(b) AS target_type
        LIMIT 50
        """
        
        try:
            result = self.neo4j_service.session.run(query, record_ids=record_ids)
            for record in result:
                graph_evidence.append({
                    "source_entity": {"id": record["source_id"], "label": record["source_label"], "type": record["source_type"]},
                    "relationship": {"type": record["rel_type"].lower(), "confidence": record["confidence"], "sourceRecord": record["sourceRecord"]},
                    "target_entity": {"id": record["target_id"], "label": record["target_label"], "type": record["target_type"]}
                })
        except Exception as e:
            # If graph fetch fails, we still return the document evidence
            print(f"Warning: Failed to fetch graph context: {e}")
            
        return {
            "document_evidence": document_evidence,
            "graph_evidence": graph_evidence
        }
