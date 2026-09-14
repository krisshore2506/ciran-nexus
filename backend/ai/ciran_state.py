from typing import TypedDict, List, Dict, Any, Optional

class CIRANGraphState(TypedDict):
    query: str
    query_type: str # 'EVIDENCE', 'NETWORK', 'MIXED'
    requested_capabilities: List[str] # e.g. ['EVIDENCE', 'NETWORK', 'CORRELATION', 'RISK']
    entity_ids: List[str]
    
    # Agent Results
    evidence_result: Dict[str, Any]
    network_result: Dict[str, Any]
    correlation_result: Dict[str, Any]
    risk_result: Dict[str, Any]
    
    # Aggregation & Validation
    fused_context: Dict[str, Any]
    validation_status: str # 'SUFFICIENT', 'PARTIAL', 'INSUFFICIENT', 'PENDING'
    final_response: Optional[Any] # CopilotResponse
    
    # Traceability & Errors
    source_references: List[str]
    errors: List[str]
