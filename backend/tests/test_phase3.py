import pytest
from models.domain import Entity, Relation, Attribute
from services.relationship_engine import RelationshipEngine
from services.entity_resolution import EntityResolutionService
from services.graph_intelligence import GraphIntelligenceService
from services.temporal_analysis import TemporalAnalysisService
from services.risk_engine import RiskEngine

def test_entity_resolution_no_match():
    engine = RelationshipEngine()
    er = EntityResolutionService(engine)
    
    e1 = Entity(id="PAYSIM-1", type="phone", label="Phone 123", subtitle="")
    e2 = Entity(id="EMAIL-1", type="phone", label="Phone 456", subtitle="")
    
    er.process_entities([e1, e2])
    
    rels = engine.get_relations()
    assert len(rels) == 0, "Should be NO_MATCH for different phone numbers"

def test_entity_resolution_deterministic_match():
    engine = RelationshipEngine()
    er = EntityResolutionService(engine)
    
    e1 = Entity(id="PAYSIM-1", type="phone", label="Phone 123", subtitle="", attributes=[Attribute(label="phone_number", value="1234567890")])
    e2 = Entity(id="EMAIL-1", type="phone", label="Phone 123", subtitle="", attributes=[Attribute(label="phone_number", value="1234567890")])
    
    er.process_entities([e1, e2])
    
    rels = engine.get_relations()
    assert len(rels) == 1
    assert rels[0].type == "SAME_AS"
    assert rels[0].sourceRecord == "RESOLUTION_ENGINE"
    assert "identical" in rels[0].label.lower()

def test_entity_resolution_namespace_isolation():
    engine = RelationshipEngine()
    er = EntityResolutionService(engine)
    
    # Same namespace, should not match
    e1 = Entity(id="PAYSIM-1", type="account", label="Acc 1", subtitle="", attributes=[Attribute(label="account_id", value="A123")])
    e2 = Entity(id="PAYSIM-2", type="account", label="Acc 2", subtitle="", attributes=[Attribute(label="account_id", value="A123")])
    
    er.process_entities([e1, e2])
    
    rels = engine.get_relations()
    assert len(rels) == 0, "Intra-dataset merge should be blocked"

from unittest.mock import MagicMock

def test_graph_multi_hop_and_provenance():
    mock_neo4j = MagicMock()
    mock_neo4j.find_shortest_path.return_value = {
        "path": ["A", "B", "C"],
        "relationships": [
            {"sourceRecord": "REC-1"},
            {"sourceRecord": "REC-2"}
        ]
    }
    gi = GraphIntelligenceService(mock_neo4j)
    
    path, evidence = gi.find_shortest_path("A", "C")
    assert path == ["A", "B", "C"]
    assert set(evidence) == {"REC-1", "REC-2"}
    
def test_temporal_analysis_burst():
    engine = RelationshipEngine()
    ta = TemporalAnalysisService(engine)
    
    ent = Entity(id="E-1", type="account", label="A", subtitle="")
    
    # 5 relations at timestamp T1
    for i in range(5):
        engine.add_relation("E-1", f"T-{i}", "financial", "tx", 90, f"REC-{i}", timestamp="2024-01-01T12:00:00")
        
    insights = ta.generate_insights([ent])
    assert len(insights) == 1
    assert insights[0].category == "Temporal Burst"
    assert set(insights[0].evidence) == {"REC-0", "REC-1", "REC-2", "REC-3", "REC-4"}

def test_risk_engine_explainable_factors():
    engine = RelationshipEngine()
    re = RiskEngine(engine)
    
    ent = Entity(id="E-1", type="account", label="A", subtitle="", attributes=[Attribute(label="isFraud", value="1")])
    
    # Add a network connection
    engine.add_relation("E-1", "E-2", "financial", "tx", 90, "REC-1")
    
    processed_ent = re.calculate_entity_priority(ent)
    
    labels = [f.label for f in processed_ent.priorityFactors]
    assert "Dataset fraud flag (PaySim)" in labels
    assert "Network connectivity" in labels
    assert processed_ent.priorityBand == "MEDIUM" or processed_ent.priorityBand == "HIGH"
