from ai.ciran_state import CIRANGraphState
from services.vector_search import VectorSearchService

class EvidenceAgent:
    def __init__(self, vector_search: VectorSearchService):
        self.vector_search = vector_search

    def execute(self, state: CIRANGraphState) -> CIRANGraphState:
        result = {
            "agent": "evidence",
            "status": "SUCCESS",
            "evidence": [],
            "source_references": [],
            "errors": []
        }
        
        try:
            hits = self.vector_search.search(state["query"], top_k=5)
            result["evidence"] = hits
            result["source_references"] = [h.get("record_id") for h in hits if h.get("record_id")]
            
            if not hits:
                result["status"] = "NO_EVIDENCE"
                
            state["source_references"].extend(result["source_references"])
        except Exception as e:
            result["status"] = "ERROR"
            result["errors"].append(str(e))
            state["errors"].append(f"EvidenceAgent: {str(e)}")
            
        state["evidence_result"] = result
        return state
