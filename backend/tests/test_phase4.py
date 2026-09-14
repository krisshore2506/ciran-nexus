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

from models.domain import RetrievalResult

def test_query_parser_intent():
    parser = QueryParser()
    state_entities = [Entity(id="CASE-101", label="Fraud", subtitle="Mock Case", type="case")]
    
    sq = parser.parse_query("summarize case-101 please", state_entities)
    assert sq.intent == "SUMMARIZE_CASE"
    assert len(sq.entities) == 1
    assert sq.entities[0] == "CASE-101"

def test_query_parser_insufficient_evidence():
    parser = QueryParser()
    state_entities = [Entity(id="CASE-101", label="Fraud", subtitle="Mock Case", type="case")]
    
    sq = parser.parse_query("who is John Doe?", state_entities)
    assert sq.intent == "ENTITY_CONTEXT"
    assert len(sq.entities) == 0 # Should not fabricate John Doe

def test_copilot_hallucination_safety():
    parser = QueryParser()
    llm = LLMService()
    state_entities = [Entity(id="CASE-101", label="Fraud Case 1", subtitle="Mock Case", type="case")]
    sq = parser.parse_query("what about John Doe?", state_entities)
    
    retrieval_result = RetrievalResult(retrieval_notes=["Insufficient evidence available"])
    res = llm.generate_copilot_response_with_result("what about John Doe?", sq, [], retrieval_result)
    assert "Insufficient evidence" in res.summary

def test_copilot_evidence_grounding():
    parser = QueryParser()
    llm = LLMService()
    target_ent = Entity(id="PAYSIM-123", label="Account 123", subtitle="Mock Account", type="account", priority=90, priorityBand="HIGH", priorityFactors=[{"label": "fraud flag", "weight": 90}])
    
    sq = parser.parse_query("why is paysim-123 flagged?", [target_ent])
    retrieval_result = RetrievalResult(evidence=["REC-1"], retrieval_notes=["DIRECT_CONNECTION"])
    
    res = llm.generate_copilot_response_with_result("why is paysim-123 flagged?", sq, [target_ent], retrieval_result)
    assert "Account 123" in res.summary or "PAYSIM-123" in res.summary or (res.derived_findings and "fraud flag" in res.derived_findings[0].lower())
    assert "REC-1" in res.evidence
