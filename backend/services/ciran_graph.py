from langgraph.graph import StateGraph, END
from ai.ciran_state import CIRANGraphState
from services.vector_search import VectorSearchService
from services.neo4j_graph_service import Neo4jGraphService
from services.context_builder import ContextBuilder
from ai.llm_service import LLMService
from models.domain import CopilotResponse, StructuredQuery, Entity
from sqlalchemy.orm import Session
import json

class CIRANGraphService:
    def __init__(self, db: Session, neo4j_session):
        self.db = db
        self.neo4j_session = neo4j_session
        self.vector_search = VectorSearchService(db)
        self.neo4j_graph = Neo4jGraphService(neo4j_session)
        self.context_builder = ContextBuilder(self.neo4j_graph)
        self.llm_service = LLMService()

        # Build Graph
        builder = StateGraph(CIRANGraphState)
        
        # Add Nodes
        builder.add_node("query_understanding", self._query_understanding)
        builder.add_node("vector_retrieval", self._vector_retrieval)
        builder.add_node("graph_retrieval", self._graph_retrieval)
        builder.add_node("context_fusion", self._context_fusion)
        builder.add_node("evidence_validation", self._evidence_validation)
        builder.add_node("generate_answer", self._generate_answer)
        builder.add_node("safe_no_evidence", self._safe_no_evidence)

        # Edges
        builder.set_entry_point("query_understanding")
        
        builder.add_conditional_edges(
            "query_understanding",
            self._route_after_understanding,
            {
                "vector_retrieval": "vector_retrieval",
                "graph_retrieval": "graph_retrieval"
            }
        )
        
        builder.add_conditional_edges(
            "vector_retrieval",
            self._route_after_vector,
            {
                "graph_retrieval": "graph_retrieval",
                "context_fusion": "context_fusion"
            }
        )
        
        builder.add_edge("graph_retrieval", "context_fusion")
        builder.add_edge("context_fusion", "evidence_validation")
        
        builder.add_conditional_edges(
            "evidence_validation",
            self._route_after_validation,
            {
                "generate_answer": "generate_answer",
                "safe_no_evidence": "safe_no_evidence"
            }
        )
        
        builder.add_edge("generate_answer", END)
        builder.add_edge("safe_no_evidence", END)
        
        self.graph = builder.compile()

    def invoke(self, query: str) -> CopilotResponse:
        initial_state = {
            "query": query,
            "query_type": "EVIDENCE",
            "entity_ids": [],
            "vector_evidence": [],
            "graph_context": [],
            "fused_context": {},
            "evidence_status": "PENDING",
            "response": None,
            "source_references": [],
            "errors": []
        }
        
        final_state = self.graph.invoke(initial_state)
        return final_state["response"]

    # --- Node Implementations ---
    
    def _query_understanding(self, state: CIRANGraphState) -> CIRANGraphState:
        query = state["query"].lower()
        
        # Simple deterministic classifier
        # Do not use state.py or LLM for simple understanding
        if "connect" in query or "network" in query or "relationship" in query or "path" in query:
            if "what" in query or "where" in query or "how" in query:
                state["query_type"] = "MIXED"
            else:
                state["query_type"] = "GRAPH"
        else:
            state["query_type"] = "EVIDENCE"
            
        return state

    def _route_after_understanding(self, state: CIRANGraphState) -> str:
        if state["query_type"] in ["MIXED", "EVIDENCE"]:
            return "vector_retrieval"
        return "graph_retrieval"

    def _vector_retrieval(self, state: CIRANGraphState) -> CIRANGraphState:
        try:
            results = self.vector_search.search(state["query"], top_k=5)
            state["vector_evidence"] = results
            state["source_references"].extend([r["record_id"] for r in results])
        except Exception as e:
            state["errors"].append(f"Vector retrieval failed: {str(e)}")
        return state

    def _route_after_vector(self, state: CIRANGraphState) -> str:
        if state["query_type"] == "MIXED":
            return "graph_retrieval"
        return "context_fusion"

    def _graph_retrieval(self, state: CIRANGraphState) -> CIRANGraphState:
        try:
            # If we already have vector evidence, context_builder does this securely.
            # But graph_retrieval might also query direct neo4j multi-hop if it's a GRAPH query.
            # For simplicity, if we have record_ids, we will let context_fusion handle the provenance.
            # If it's a pure GRAPH query, we might just query Neo4j.
            # For now, we will rely on context_builder for evidence-grounded graph.
            pass
        except Exception as e:
            state["errors"].append(f"Graph retrieval failed: {str(e)}")
        return state

    def _context_fusion(self, state: CIRANGraphState) -> CIRANGraphState:
        if state["vector_evidence"]:
            context = self.context_builder.build_context(state["vector_evidence"])
            state["fused_context"] = context
        else:
            state["fused_context"] = {"document_evidence": [], "graph_evidence": []}
        return state

    def _evidence_validation(self, state: CIRANGraphState) -> CIRANGraphState:
        fused = state["fused_context"]
        docs = fused.get("document_evidence", [])
        graphs = fused.get("graph_evidence", [])
        
        if not docs and not graphs:
            state["evidence_status"] = "NO_EVIDENCE"
        elif len(docs) < 2 and not graphs:
            state["evidence_status"] = "PARTIAL_EVIDENCE"
        else:
            state["evidence_status"] = "SUFFICIENT_EVIDENCE"
            
        return state

    def _route_after_validation(self, state: CIRANGraphState) -> str:
        if state["evidence_status"] == "NO_EVIDENCE":
            return "safe_no_evidence"
        return "generate_answer"

    def _generate_answer(self, state: CIRANGraphState) -> CIRANGraphState:
        try:
            # Create a mock StructuredQuery and RetrievalResult just to reuse LLMService
            from models.domain import RetrievalResult
            
            sq = StructuredQuery(intent="EVIDENCE", confidence=0.9, entities=[], ambiguous=False, time_range=None)
            rr = RetrievalResult()
            
            fused = state["fused_context"]
            rr.evidence = list(set([d["record_id"] for d in fused.get("document_evidence", [])]))
            rr.retrieval_notes.append(f"DOCUMENT_EVIDENCE: {json.dumps(fused.get('document_evidence', []))}")
            rr.retrieval_notes.append(f"GRAPH_EVIDENCE: {json.dumps(fused.get('graph_evidence', []))}")
            
            res = self.llm_service.generate_copilot_response_with_result(
                state["query"], sq, [], rr
            )
            state["response"] = res
        except Exception as e:
            state["errors"].append(str(e))
            state["response"] = CopilotResponse(
                summary="An error occurred while generating the response.",
                chips=["Error"],
                confidence=0,
                caution="System Failure",
                intent="UNKNOWN"
            )
        return state

    def _safe_no_evidence(self, state: CIRANGraphState) -> CIRANGraphState:
        state["response"] = CopilotResponse(
            summary="Insufficient evidence was found in the available CIRAN records to answer this query.",
            chips=["No Evidence"],
            confidence=100,
            caution="Generated by AI. Verify all source records.",
            intent="UNKNOWN"
        )
        return state
