from typing import TypedDict, List, Dict, Any, Optional

class CIRANGraphState(TypedDict):
    query: str
    query_type: str
    entity_ids: List[str]
    vector_evidence: List[Dict[str, Any]]
    graph_context: List[Dict[str, Any]]
    fused_context: Dict[str, Any]
    evidence_status: str
    response: Optional[Any]
    source_references: List[str]
    errors: List[str]
