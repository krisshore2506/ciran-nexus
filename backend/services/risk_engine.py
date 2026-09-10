from typing import List, Dict, Any
from models.domain import Entity, Alert, PriorityFactor, PatternInsight
from services.relationship_engine import RelationshipEngine
import datetime

class RiskEngine:
    def __init__(self, relationship_engine: RelationshipEngine):
        self.relationship_engine = relationship_engine
        self.alerts: List[Alert] = []
        self.patterns: List[PatternInsight] = []
        
    def calculate_entity_priority(self, entity: Entity) -> Entity:
        neighbors = self.relationship_engine.get_neighbors(entity.id)
        
        factors = []
        score = 0
        
        # Factor 1: Network connectivity (only direct real edges, skip RESOLUTION_ENGINE)
        real_neighbors = [n for n in neighbors if n.sourceRecord != "RESOLUTION_ENGINE"]
        if len(real_neighbors) > 0:
            weight = min(len(real_neighbors) * 5, 30)
            factors.append(PriorityFactor(label="Network connectivity", weight=weight))
            score += weight
            
        # Factor 2: Cross-case presence
        case_links = [n for n in real_neighbors if "CASE" in n.target or "CASE" in n.source]
        if len(case_links) > 1:
            weight = len(case_links) * 10
            factors.append(PriorityFactor(label="Cross-case links", weight=weight))
            score += weight
            
        # Factor 3: Dataset-specific risk signals (PaySim)
        if entity.attributes:
            for attr in entity.attributes:
                if attr.label == "isFraud" and attr.value == "1":
                    # Fraud flag from PaySim is a risk signal, but does not mean "criminal" on its own
                    weight = 25
                    factors.append(PriorityFactor(label="Dataset fraud flag (PaySim)", weight=weight))
                    score += weight
                elif attr.label == "isFlaggedFraud" and attr.value == "1":
                    weight = 15
                    factors.append(PriorityFactor(label="Dataset flagged behavior (PaySim)", weight=weight))
                    score += weight
            
        entity.priority = score
        if score >= 60:
            entity.priorityBand = "HIGH"
        elif score >= 30:
            entity.priorityBand = "MEDIUM"
        else:
            entity.priorityBand = "LOW"
            
        entity.priorityFactors = factors
        entity.relationships = len(real_neighbors)
        return entity
        
    def generate_alerts(self, entities: List[Entity]):
        for e in entities:
            if getattr(e, "priorityBand", "") == "HIGH":
                self.alerts.append(Alert(
                    id=f"AL-{len(self.alerts)+1}",
                    severity="high",
                    title="High priority entity identified",
                    explanation=f"Entity {e.label} has accumulated a high priority score based on explainable factors.",
                    case="Multiple",
                    timestamp=datetime.datetime.now().isoformat(),
                    confidence=85,
                    entities=[e.id]
                ))
                
        return self.alerts
