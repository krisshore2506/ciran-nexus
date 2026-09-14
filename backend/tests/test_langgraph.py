import pytest
from unittest.mock import MagicMock
from services.ciran_graph import CIRANGraphService
from models.domain import CopilotResponse

def test_graph_construction():
    mock_db = MagicMock()
    mock_neo4j = MagicMock()
    
    # Just constructing it should succeed without errors
    service = CIRANGraphService(mock_db, mock_neo4j)
    assert service.graph is not None

def test_query_understanding_node():
    mock_db = MagicMock()
    mock_neo4j = MagicMock()
    service = CIRANGraphService(mock_db, mock_neo4j)
    
    # Evidence query
    state = {"query": "Find the passport", "query_type": "", "errors": []}
    state = service._query_understanding(state)
    assert state["query_type"] == "EVIDENCE"
    
    # Network query
    state = {"query": "How is Alice connected to Bob?", "query_type": "", "errors": []}
    state = service._query_understanding(state)
    assert state["query_type"] == "MIXED"

def test_no_evidence_routing():
    mock_db = MagicMock()
    mock_neo4j = MagicMock()
    service = CIRANGraphService(mock_db, mock_neo4j)
    
    state = {
        "fused_context": {"document_evidence": [], "graph_evidence": []},
        "evidence_status": "",
        "errors": []
    }
    
    state = service._evidence_validation(state)
    assert state["evidence_status"] == "NO_EVIDENCE"
    
    route = service._route_after_validation(state)
    assert route == "safe_no_evidence"
    
    state = service._safe_no_evidence(state)
    assert "response" in state
    assert isinstance(state["response"], CopilotResponse)
    assert state["response"].chips == ["No Evidence"]

def test_generate_answer_node():
    mock_db = MagicMock()
    mock_neo4j = MagicMock()
    service = CIRANGraphService(mock_db, mock_neo4j)
    
    # Mock the LLM service to avoid actual API calls
    service.llm_service.generate_copilot_response_with_result = MagicMock(
        return_value=CopilotResponse(
            summary="Test Response",
            chips=["Test"],
            confidence=100,
            caution="Test Caution",
            intent="EVIDENCE"
        )
    )
    
    state = {
        "query": "Test",
        "fused_context": {
            "document_evidence": [{"record_id": "R1", "chunk_id": "C1", "text": "test"}],
            "graph_evidence": []
        },
        "errors": []
    }
    
    state = service._generate_answer(state)
    assert state["response"].summary == "Test Response"
