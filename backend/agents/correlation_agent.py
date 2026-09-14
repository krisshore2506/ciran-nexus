from ai.ciran_state import CIRANGraphState
from typing import Dict, Any

class CorrelationAgent:
    def execute(self, state: CIRANGraphState) -> CIRANGraphState:
        result = {
            "agent": "correlation",
            "status": "SUCCESS",
            "correlations": [],
            "supporting_evidence": [],
            "confidence": 0,
            "source_references": [],
            "errors": []
        }
        
        try:
            # Consume Evidence and Network Agent outputs
            evidence = state.get("evidence_result", {}).get("evidence", [])
            network_nodes = state.get("network_result", {}).get("nodes", [])
            
            if not evidence and not network_nodes:
                result["status"] = "NO_EVIDENCE"
                state["correlation_result"] = result
                return state

            # Basic deterministic stub for multi-agent flow
            # In a full implementation, this wraps the legacy CorrelationEngine safely
            if len(network_nodes) > 1 and len(evidence) > 0:
                result["correlations"].append({
                    "summary": "Detected overlapping entities based on combined graph and vector evidence.",
                    "type": "Graph-Evidence Overlap"
                })
                result["confidence"] = 75
                # Inherit source references
                ev_refs = state.get("evidence_result", {}).get("source_references", [])
                net_refs = state.get("network_result", {}).get("source_references", [])
                result["source_references"] = list(set(ev_refs + net_refs))
            else:
                result["status"] = "NO_EVIDENCE"
                
            state["source_references"].extend(result["source_references"])
            
        except Exception as e:
            result["status"] = "ERROR"
            result["errors"].append(str(e))
            state["errors"].append(f"CorrelationAgent: {str(e)}")
            
        state["correlation_result"] = result
        return state
