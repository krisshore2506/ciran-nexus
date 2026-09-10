import pytest
from models.domain import Entity
from services.query_parser import QueryParser
from ai.llm_service import LLMService

class MockState:
    def __init__(self):
        self.entities = [
            Entity(id="CASE-101", label="Fraud Case 1", subtitle="Mock Case", type="case"),
            Entity(id="PAYSIM-123", label="Account 123", subtitle="Mock Account", type="account", priority=30, priorityBand="MEDIUM", priorityFactors=[
                {"label": "Dataset fraud flag (PaySim)", "weight": 25}
            ])
        ]
        self.cross_case_links = []
        self.patterns = []
        self.alerts = []
        
        class MockRelEngine:
            def get_neighbors(self, eid):
                class MockNode:
                    def __init__(self, sr):
                        self.sourceRecord = sr
                return [MockNode("REC-1")]
        self.relationship_engine = MockRelEngine()

def test_query_parser_intent():
    parser = QueryParser()
    state_entities = [Entity(id="CASE-101", label="Fraud", subtitle="Mock Case", type="case")]
    
    intent, entities = parser.parse_query("summarize case-101 please", state_entities)
    assert intent == "SUMMARIZE_CASE"
    assert len(entities) == 1
    assert entities[0].id == "CASE-101"

def test_query_parser_insufficient_evidence():
    parser = QueryParser()
    state_entities = [Entity(id="CASE-101", label="Fraud", subtitle="Mock Case", type="case")]
    
    intent, entities = parser.parse_query("who is John Doe?", state_entities)
    assert intent == "ENTITY_CONTEXT"
    assert len(entities) == 0 # Should not fabricate John Doe

def test_copilot_hallucination_safety():
    state = MockState()
    parser = QueryParser()
    llm = LLMService()
    
    res = llm.generate_copilot_response("what about John Doe?", state, parser)
    assert "Insufficient evidence" in res.summary
    assert res.confidence == 0

def test_copilot_evidence_grounding():
    state = MockState()
    parser = QueryParser()
    llm = LLMService()
    
    res = llm.generate_copilot_response("why is paysim-123 flagged?", state, parser)
    assert "PAYSIM-123" in res.summary
    assert "fraud flag" in res.summary.lower()
    assert "REC-1" in res.evidence
    assert res.confidence == 90
