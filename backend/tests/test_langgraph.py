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
    state = {"query": "Find the passport", "query_type": "EVIDENCE", "errors": [], "requested_capabilities": []}
    state = service.supervisor.execute(state)
    assert "EVIDENCE" in state["requested_capabilities"] or state["requested_capabilities"] == []

def test_no_evidence_routing():
    mock_db = MagicMock()
    mock_neo4j = MagicMock()
    service = CIRANGraphService(mock_db, mock_neo4j)
    
    state = {
        "evidence_result": {"status": "SUCCESS", "records": []},
        "network_result": {"status": "SUCCESS", "nodes": []},
        "fused_context": {},
        "validation_status": "PENDING",
        "errors": []
    }
    
    state = service._validator_node(state)
    assert state["validation_status"] in ["INSUFFICIENT", "SUFFICIENT"]
    
    route = service._route_from_validator(state)
    assert route in ["safe_response", "generator"]
    
    state = service._safe_response_node(state)
    assert "final_response" in state
    assert isinstance(state["final_response"], CopilotResponse)
    assert state["final_response"].chips == ["No Evidence"]

def test_generate_answer_node():
    mock_db = MagicMock()
    mock_neo4j = MagicMock()
    service = CIRANGraphService(mock_db, mock_neo4j)
    
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
        "query_type": "EVIDENCE",
        "fused_context": {
            "evidence": {"records": [{"id": "R1"}]}
        },
        "errors": [],
        "source_references": []
    }
    
    state = service._generator_node(state)
    assert state["final_response"].summary == "Test Response"
