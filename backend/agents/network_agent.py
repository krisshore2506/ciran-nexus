from ai.ciran_state import CIRANGraphState
from services.neo4j_graph_service import Neo4jGraphService
from services.context_builder import ContextBuilder

class NetworkAgent:
    def __init__(self, neo4j_graph: Neo4jGraphService):
        self.neo4j_graph = neo4j_graph
        self.context_builder = ContextBuilder(neo4j_graph)

    def execute(self, state: CIRANGraphState) -> CIRANGraphState:
        result = {
            "agent": "network",
            "status": "SUCCESS",
            "nodes": [],
            "relationships": [],
            "metrics": {},
            "source_references": [],
            "errors": []
        }
        
        try:
            # We use context_builder if we have evidence from the EvidenceAgent,
            # otherwise we might attempt a raw network query if entities are known.
            evidence = state.get("evidence_result", {}).get("evidence", [])
            
            if evidence:
                graph_context = self.context_builder.build_context(evidence).get("graph_evidence", [])
                result["nodes"] = graph_context # simplified for agent contract
                # collect distinct source records from graph properties if available
                
            if not result["nodes"]:
                result["status"] = "NO_EVIDENCE"
                
        except Exception as e:
            result["status"] = "ERROR"
            result["errors"].append(str(e))
            state["errors"].append(f"NetworkAgent: {str(e)}")
            
        state["network_result"] = result
        return state
