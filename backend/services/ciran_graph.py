from langgraph.graph import StateGraph, END
from ai.ciran_state import CIRANGraphState
from sqlalchemy.orm import Session
import json

from services.vector_search import VectorSearchService
from services.neo4j_graph_service import Neo4jGraphService
from ai.llm_service import LLMService

from agents.supervisor_agent import SupervisorAgent
from agents.evidence_agent import EvidenceAgent
from agents.network_agent import NetworkAgent
from agents.correlation_agent import CorrelationAgent
from agents.risk_agent import RiskAgent
from agents.evidence_validator import EvidenceValidator
from models.domain import CopilotResponse, StructuredQuery, RetrievalResult

class CIRANGraphService:
    def __init__(self, db: Session, neo4j_session):
        self.db = db
        self.neo4j_session = neo4j_session
        
        # Core Services
        self.vector_search = VectorSearchService(db)
        self.neo4j_graph = Neo4jGraphService(neo4j_session)
        self.llm_service = LLMService()
        
        # Agents
        self.supervisor = SupervisorAgent()
        self.evidence_agent = EvidenceAgent(self.vector_search)
        self.network_agent = NetworkAgent(self.neo4j_graph)
        self.correlation_agent = CorrelationAgent(self.neo4j_graph)
        self.risk_agent = RiskAgent()
        self.validator = EvidenceValidator()

        # Build Graph
        builder = StateGraph(CIRANGraphState)
        
        # Nodes
        builder.add_node("supervisor", self._supervisor_node)
        builder.add_node("evidence", self._evidence_node)
        builder.add_node("network", self._network_node)
        builder.add_node("correlation", self._correlation_node)
        builder.add_node("risk", self._risk_node)
        builder.add_node("aggregator", self._aggregator_node)
        builder.add_node("validator", self._validator_node)
        builder.add_node("generator", self._generator_node)
        builder.add_node("safe_response", self._safe_response_node)

        # Edges
        builder.set_entry_point("supervisor")
        
        # Supervisor conditional routing
        builder.add_conditional_edges(
            "supervisor",
            self._route_from_supervisor,
            {
                "evidence": "evidence",
                "network": "network",
                "aggregator": "aggregator"
            }
        )
        
        # Evidence conditional routing
        builder.add_conditional_edges(
            "evidence",
            self._route_from_evidence,
            {
                "network": "network",
                "correlation": "correlation",
                "risk": "risk",
                "aggregator": "aggregator"
            }
        )
        
        # Network conditional routing
        builder.add_conditional_edges(
            "network",
            self._route_from_network,
            {
                "correlation": "correlation",
                "risk": "risk",
                "aggregator": "aggregator"
            }
        )
        
        # Correlation conditional routing
        builder.add_conditional_edges(
            "correlation",
            self._route_from_correlation,
            {
                "risk": "risk",
                "aggregator": "aggregator"
            }
        )
        
        # Risk -> Aggregator
        builder.add_edge("risk", "aggregator")
        
        # Aggregator -> Validator
        builder.add_edge("aggregator", "validator")
        
        # Validator -> Generate or Safe
        builder.add_conditional_edges(
            "validator",
            self._route_from_validator,
            {
                "generator": "generator",
                "safe_response": "safe_response"
            }
        )
        
        builder.add_edge("generator", END)
        builder.add_edge("safe_response", END)
        
        self.graph = builder.compile()

    def invoke(self, query: str) -> CopilotResponse:
        initial_state = {
            "query": query,
            "query_type": "EVIDENCE",
            "requested_capabilities": [],
            "entity_ids": [],
            "evidence_result": {},
            "network_result": {},
            "correlation_result": {},
            "risk_result": {},
            "fused_context": {},
            "validation_status": "PENDING",
            "final_response": None,
            "source_references": [],
            "errors": []
        }
        
        final_state = self.graph.invoke(initial_state)
        return final_state["final_response"]

    # --- Node Wrappers ---
    def _supervisor_node(self, state: CIRANGraphState):
        return self.supervisor.execute(state)
        
    def _evidence_node(self, state: CIRANGraphState):
        return self.evidence_agent.execute(state)
        
    def _network_node(self, state: CIRANGraphState):
        return self.network_agent.execute(state)
        
    def _correlation_node(self, state: CIRANGraphState):
        return self.correlation_agent.execute(state)
        
    def _risk_node(self, state: CIRANGraphState):
        return self.risk_agent.execute(state)
        
    def _aggregator_node(self, state: CIRANGraphState):
        # Flatten all agent results into fused_context
        state["fused_context"] = {
            "evidence": state.get("evidence_result", {}),
            "network": state.get("network_result", {}),
            "correlation": state.get("correlation_result", {}),
            "risk": state.get("risk_result", {})
        }
        return state
        
    def _validator_node(self, state: CIRANGraphState):
        return self.validator.execute(state)

    def _generator_node(self, state: CIRANGraphState):
        try:
            sq = StructuredQuery(intent=state.get("query_type", "EVIDENCE"), confidence=0.9, entities=[], ambiguous=False, time_range=None)
            rr = RetrievalResult()
            
            fused = state["fused_context"]
            rr.evidence = state.get("source_references", [])
            rr.retrieval_notes.append(f"MULTI_AGENT_CONTEXT: {json.dumps(fused)}")
            
            res = self.llm_service.generate_copilot_response_with_result(
                state["query"], sq, [], rr
            )
            state["final_response"] = res
        except Exception as e:
            state["errors"].append(str(e))
            state["final_response"] = CopilotResponse(
                summary="An error occurred while generating the response.",
                chips=["Error"],
                confidence=0,
                caution="System Failure",
                intent="UNKNOWN"
            )
        return state

    def _safe_response_node(self, state: CIRANGraphState):
        state["final_response"] = CopilotResponse(
            summary="Insufficient evidence was found in the available CIRAN records to fully answer this query.",
            chips=["No Evidence"],
            confidence=100,
            caution="Generated by AI. Verify all source records.",
            intent="UNKNOWN"
        )
        return state

    # --- Routers ---
    def _route_from_supervisor(self, state: CIRANGraphState) -> str:
        req = set(state.get("requested_capabilities", []))
        if "EVIDENCE" in req: return "evidence"
        if "NETWORK" in req: return "network"
        return "aggregator"

    def _route_from_evidence(self, state: CIRANGraphState) -> str:
        req = set(state.get("requested_capabilities", []))
        if "NETWORK" in req: return "network"
        if "CORRELATION" in req: return "correlation"
        if "RISK" in req: return "risk"
        return "aggregator"

    def _route_from_network(self, state: CIRANGraphState) -> str:
        req = set(state.get("requested_capabilities", []))
        if "CORRELATION" in req: return "correlation"
        if "RISK" in req: return "risk"
        return "aggregator"

    def _route_from_correlation(self, state: CIRANGraphState) -> str:
        req = set(state.get("requested_capabilities", []))
        if "RISK" in req: return "risk"
        return "aggregator"

    def _route_from_validator(self, state: CIRANGraphState) -> str:
        if state.get("validation_status") == "INSUFFICIENT":
            return "safe_response"
        return "generator"
