import pytest
import os
import sys
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from config.neo4j import get_neo4j, neo4j_driver
from services.neo4j_graph_service import Neo4jGraphService

client = TestClient(app)

@pytest.fixture(scope="module")
def neo4j_session():
    neo4j_driver.connect()
    session = neo4j_driver.get_session()
    yield session
    session.close()
    neo4j_driver.close()

def test_neo4j_connection(neo4j_session):
    result = neo4j_session.run("RETURN 1 AS n").single()
    assert result["n"] == 1

def test_constraint_creation(neo4j_session):
    service = Neo4jGraphService(neo4j_session)
    service.create_constraints()
    # If this doesn't throw an error, we assume success
    assert True

def test_direct_neighbors(neo4j_session):
    service = Neo4jGraphService(neo4j_session)
    result = service.get_direct_neighbors("P-RAVI")
    assert "nodes" in result
    assert "relationships" in result
    # Assuming seed data contains P-RAVI and its connections
    # We can just check that it runs successfully
    assert isinstance(result["nodes"], list)
    assert isinstance(result["relationships"], list)

def test_multi_hop_traversal(neo4j_session):
    service = Neo4jGraphService(neo4j_session)
    result = service.get_multi_hop_network("P-RAVI", max_depth=2)
    assert "nodes" in result
    assert "relationships" in result

def test_invalid_depth(neo4j_session):
    service = Neo4jGraphService(neo4j_session)
    # Depth > 5 should fall back to 3
    result = service.get_multi_hop_network("P-RAVI", max_depth=10)
    assert "nodes" in result

def test_shortest_path(neo4j_session):
    service = Neo4jGraphService(neo4j_session)
    # Should work if they are connected, else return None
    path_info = service.find_shortest_path("P-RAVI", "P-ARJUN")
    if path_info:
        assert "path" in path_info
        assert "nodes" in path_info
        assert "relationships" in path_info
        assert "path_length" in path_info
        assert path_info["source"] == "P-RAVI"
        assert path_info["target"] == "P-ARJUN"

def test_no_path_scenario(neo4j_session):
    service = Neo4jGraphService(neo4j_session)
    path_info = service.find_shortest_path("P-RAVI", "NON-EXISTENT-NODE")
    assert path_info is None

def test_common_connections(neo4j_session):
    service = Neo4jGraphService(neo4j_session)
    common = service.get_common_connections("P-RAVI", "P-ARJUN")
    assert isinstance(common, list)

def test_case_network(neo4j_session):
    service = Neo4jGraphService(neo4j_session)
    network = service.get_case_network("CASE-203")
    assert "nodes" in network
    assert "relationships" in network

def test_graph_metrics(neo4j_session):
    service = Neo4jGraphService(neo4j_session)
    metrics = service.get_graph_metrics("P-RAVI")
    assert "degree" in metrics
    assert "case_count" in metrics

def test_api_network_endpoints():
    response = client.get("/api/network", params={"limit": 10})
    assert response.status_code == 200
    assert "nodes" in response.json()
    assert "edges" in response.json()

    response = client.get("/api/network/entity/P-RAVI/network", params={"max_depth": 2})
    assert response.status_code == 200
    assert "nodes" in response.json()
    assert "edges" in response.json()

    response = client.get("/api/network/shortest-path", params={"source": "P-RAVI", "target": "P-ARJUN"})
    assert response.status_code == 200
    
    response = client.get("/api/network/common-connections", params={"source": "P-RAVI", "target": "P-ARJUN"})
    assert response.status_code == 200
    assert "common_connections" in response.json()
