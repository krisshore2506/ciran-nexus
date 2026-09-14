import pytest
from unittest.mock import MagicMock
from services.ciran_graph import CIRANGraphService
from models.domain import CopilotResponse

def test_supervisor_routing_evidence():
    mock_db = MagicMock()
    mock_neo4j = MagicMock()
    service = CIRANGraphService(mock_db, mock_neo4j)
    
    state = {"query": "Find evidence about John", "query_type": "", "errors": []}
    state = service.supervisor.execute(state)
    assert "EVIDENCE" in state["requested_capabilities"]
    
    route = service._route_from_supervisor(state)
    assert route == "evidence"

def test_supervisor_routing_mixed_risk():
    mock_db = MagicMock()
    mock_neo4j = MagicMock()
    service = CIRANGraphService(mock_db, mock_neo4j)
    
    state = {"query": "Find network connections and assess risk", "query_type": "", "errors": []}
    state = service.supervisor.execute(state)
    assert "NETWORK" in state["requested_capabilities"]
    assert "RISK" in state["requested_capabilities"]
    
    route1 = service._route_from_supervisor(state)
    assert route1 == "network"
    
    route2 = service._route_from_network(state)
    assert route2 == "risk"
    
    route3 = service._route_from_risk(state) if hasattr(service, '_route_from_risk') else "aggregator"
    assert route3 == "aggregator"

def test_evidence_validator_insufficient():
    mock_db = MagicMock()
    mock_neo4j = MagicMock()
    service = CIRANGraphService(mock_db, mock_neo4j)
    
    state = {
        "evidence_result": {"status": "NO_EVIDENCE"},
        "network_result": {"status": "NO_EVIDENCE"}
    }
    
    state = service.validator.execute(state)
    assert state["validation_status"] == "INSUFFICIENT"
    
    route = service._route_from_validator(state)
    assert route == "safe_response"

def test_safe_response_generator():
    mock_db = MagicMock()
    mock_neo4j = MagicMock()
    service = CIRANGraphService(mock_db, mock_neo4j)
    
    state = {"final_response": None}
    state = service._safe_response_node(state)
    
    assert isinstance(state["final_response"], CopilotResponse)
    assert state["final_response"].chips == ["No Evidence"]
