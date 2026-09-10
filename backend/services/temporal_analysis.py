from typing import List, Dict
import uuid
import datetime
from models.domain import Entity, Relation, TimelineEvent, PatternInsight
from services.relationship_engine import RelationshipEngine

class TemporalAnalysisService:
    def __init__(self, relationship_engine: RelationshipEngine):
        self.relationship_engine = relationship_engine
        
    def generate_insights(self, entities: List[Entity]) -> List[PatternInsight]:
        insights = []
        
        # Example logic: burst activity detection
        # Finds entities that have multiple interactions in exactly the same timestamp (or step for paysim)
        
        for ent in entities:
            neighbors = self.relationship_engine.get_neighbors(ent.id)
            if not neighbors:
                continue
                
            # Group by timestamp
            time_groups: Dict[str, List[Relation]] = {}
            for rel in neighbors:
                ts = rel.timestamp
                if ts:
                    if ts not in time_groups:
                        time_groups[ts] = []
                    time_groups[ts].append(rel)
            
            for ts, rels in time_groups.items():
                if len(rels) >= 5: # e.g. 5 interactions at the same time/step
                    source_ids = list(set([r.sourceRecord for r in rels if r.sourceRecord != "RESOLUTION_ENGINE"]))
                    if source_ids:
                        insights.append(PatternInsight(
                            id=f"TMP-{uuid.uuid4().hex[:8].upper()}",
                            category="Temporal Burst",
                            title="High Velocity Interaction",
                            entities=[ent.id],
                            confidence=85,
                            why=f"Entity engaged in {len(rels)} distinct interactions exactly at time/step: {ts}",
                            evidence=source_ids
                        ))
                    
        return insights
