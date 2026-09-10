import pytest
from fastapi.testclient import TestClient
from main import app
from ingestion.adapters import get_adapter
from models.unified import SourceRecord

client = TestClient(app)

def test_crime_adapter_streaming():
    adapter = get_adapter("crime", "data/sample/crime_test.csv")
    records = list(adapter.stream_records())
    
    assert len(records) == 2
    assert adapter.validation_result.accepted == 2
    
    rec = records[0]
    assert rec.source_record_id == "CR-2026-001"
    assert rec.source_dataset == "crime"
    assert len(rec.entities) == 2 # CASE and LOCATION
    assert rec.entities[0].entity_type == "CASE"
    assert rec.entities[1].entity_type == "LOCATION"
    assert len(rec.relationships) == 1
    assert rec.relationships[0].relationship_type == "OCCURRED_AT"

def test_paysim_streaming_and_max_rows():
    adapter = get_adapter("paysim", "data/sample/paysim_test.csv")
    records = list(adapter.stream_records(max_rows=2))
    
    assert len(records) == 2
    assert adapter.validation_result.accepted == 2
    
    rec = records[0]
    assert rec.source_dataset == "paysim"
    assert len(rec.entities) == 2 # 2 accounts
    assert rec.relationships[0].relationship_type == "TRANSACTION"
    assert rec.relationships[0].timestamp == "1" # Should preserve 'step' as timestamp

def test_api_ingest_email():
    payload = {
        "dataset": "email",
        "file_path": "data/sample/email_test.csv"
    }
    response = client.post("/api/ingestion/load", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["dataset"] == "email"
    assert data["stats"]["records_processed"] == 3
    assert data["adapter_validation"]["accepted"] == 3

def test_provenance_preservation():
    adapter = get_adapter("cdr", "data/sample/cdr_test.csv")
    records = list(adapter.stream_records())
    rec = records[0]
    
    assert rec.provenance.source_dataset == "itu_cdr"
    assert rec.provenance.source_file == "data/sample/cdr_test.csv"
    assert "CDR-" in rec.provenance.source_record_id
