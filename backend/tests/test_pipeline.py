from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_ingestion_and_pipeline():
    # 1. Trigger ingestion
    response = client.post("/api/ingestion/load")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # Verify stats
    stats = data["stats"]
    assert stats["records_processed"] > 0
    assert stats["entities_extracted"] > 0
    
    # 2. Check entities
    entities_res = client.get("/api/entities")
    assert entities_res.status_code == 200
    entities = entities_res.json()
    assert len(entities) > 0
    
    # 3. Check cases
    cases_res = client.get("/api/cases")
    assert cases_res.status_code == 200
    cases = cases_res.json()
    assert len(cases) > 0
    
    # 4. Check network
    network_res = client.get("/api/network")
    assert network_res.status_code == 200
    network = network_res.json()
    assert len(network["nodes"]) > 0
    assert len(network["edges"]) > 0

def test_copilot_mock():
    response = client.post("/api/copilot/query", json={"query": "What is the status of case 203 involving ravi?"})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "chips" in data

def test_evidence_has_source_records():
    # 1. Trigger ingestion
    client.post("/api/ingestion/load")
    
    # 2. Get cross-case links
    cross_res = client.get("/api/cross-case")
    cross_links = cross_res.json()
    assert len(cross_links) > 0, "No cross case links generated"
    
    # 3. Get evidence for the first link
    ev_id = cross_links[0]["evidence"][0]
    ev_res = client.get(f"/api/evidence/{ev_id}")
    assert ev_res.status_code == 200
    
    evidence = ev_res.json()
    assert "sources" in evidence
    assert len(evidence["sources"]) > 0, "Sources should not be empty!"
    
    # 4. Ensure source IDs look like the ones in the dataset
    source_ids = [s["id"] for s in evidence["sources"]]
    # Should contain things like CASE-xxx or CDR-xxx
    assert any("case" in sid.lower() or "cdr" in sid.lower() or "vehicle" in sid.lower() or "ac" in sid.lower() for sid in source_ids), f"Unexpected source IDs: {source_ids}"
