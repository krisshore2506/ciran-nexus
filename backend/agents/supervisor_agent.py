from ai.ciran_state import CIRANGraphState

class SupervisorAgent:
    def execute(self, state: CIRANGraphState) -> CIRANGraphState:
        query = state["query"].lower()
        requested = set()
        
        # Heuristics based on deterministic classification
        if "connect" in query or "network" in query or "relationship" in query or "path" in query:
            requested.add("NETWORK")
            if "what" in query or "where" in query or "how" in query or "evidence" in query:
                requested.add("EVIDENCE")
        else:
            requested.add("EVIDENCE")
            
        if "correlate" in query or "overlap" in query or "pattern" in query or "case a and case b" in query:
            requested.add("CORRELATION")
            requested.add("NETWORK") # correlation usually needs network context
            
        if "risk" in query or "threat" in query or "danger" in query:
            requested.add("RISK")
            requested.add("NETWORK") # risk evaluates network topology
            
        # Ensure we have at least one base capability
        if not requested:
            requested.add("EVIDENCE")
            
        # Map back to state
        state["requested_capabilities"] = list(requested)
        
        # Also set legacy query_type for backward compatibility if needed
        if "NETWORK" in requested and "EVIDENCE" in requested:
            state["query_type"] = "MIXED"
        elif "NETWORK" in requested:
            state["query_type"] = "GRAPH"
        else:
            state["query_type"] = "EVIDENCE"
            
        return state
