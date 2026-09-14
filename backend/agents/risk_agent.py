from ai.ciran_state import CIRANGraphState

class RiskAgent:
    def execute(self, state: CIRANGraphState) -> CIRANGraphState:
        result = {
            "agent": "risk",
            "status": "SUCCESS",
            "risk_score": 0,
            "risk_level": "LOW",
            "factors": [],
            "source_references": [],
            "errors": []
        }
        
        try:
            network_nodes = state.get("network_result", {}).get("nodes", [])
            correlations = state.get("correlation_result", {}).get("correlations", [])
            
            if not network_nodes and not correlations:
                result["status"] = "NO_EVIDENCE"
                state["risk_result"] = result
                return state

            score = 0
            
            # Simple deterministic scoring
            if len(network_nodes) >= 5:
                score += 30
                result["factors"].append({
                    "factor": "High relationship density",
                    "weight": 30,
                    "evidence": [f"Network size: {len(network_nodes)}"]
                })
            elif len(network_nodes) > 0:
                score += 10
                
            if correlations:
                score += 40
                result["factors"].append({
                    "factor": "Cross-case connections",
                    "weight": 40,
                    "evidence": ["Overlapping case entities detected"]
                })
                
            result["risk_score"] = score
            if score >= 70:
                result["risk_level"] = "HIGH"
            elif score >= 40:
                result["risk_level"] = "MEDIUM"
                
            # Inherit refs
            net_refs = state.get("network_result", {}).get("source_references", [])
            corr_refs = state.get("correlation_result", {}).get("source_references", [])
            result["source_references"] = list(set(net_refs + corr_refs))
            
            state["source_references"].extend(result["source_references"])
            
        except Exception as e:
            result["status"] = "ERROR"
            result["errors"].append(str(e))
            state["errors"].append(f"RiskAgent: {str(e)}")
            
        state["risk_result"] = result
        return state
