from ai.ciran_state import CIRANGraphState

class EvidenceValidator:
    def execute(self, state: CIRANGraphState) -> CIRANGraphState:
        ev_status = state.get("evidence_result", {}).get("status", "NO_EVIDENCE")
        net_status = state.get("network_result", {}).get("status", "NO_EVIDENCE")
        
        # Unique valid sources
        sources = [s for s in set(state.get("source_references", [])) if s]
        state["source_references"] = sources
        
        # Decide status
        if ev_status == "SUCCESS" and net_status == "SUCCESS":
            state["validation_status"] = "SUFFICIENT"
        elif ev_status == "SUCCESS" or net_status == "SUCCESS":
            state["validation_status"] = "PARTIAL"
        else:
            state["validation_status"] = "INSUFFICIENT"
            
        return state
