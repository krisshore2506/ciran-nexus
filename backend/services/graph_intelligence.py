from typing import List, Dict, Set, Tuple, Optional
from collections import deque
from models.domain import Entity, Relation, PatternInsight
from services.relationship_engine import RelationshipEngine
import uuid

class GraphIntelligenceService:
    def __init__(self, relationship_engine: RelationshipEngine):
        self.relationship_engine = relationship_engine
        
    def generate_insights(self, entities: List[Entity]) -> List[PatternInsight]:
        insights = []
        
        # Calculate centrality
        centrality = self._calculate_degree_centrality(entities)
        
        # Identify top influential entities
        if centrality:
            top_entity_id = max(centrality.keys(), key=lambda k: centrality[k])
            if centrality[top_entity_id] > 10:
                insights.append(PatternInsight(
                    id=f"PAT-{uuid.uuid4().hex[:8].upper()}",
                    category="High Connectivity",
                    title="Highly Central Entity Identified",
                    entities=[top_entity_id],
                    confidence=90,
                    why=f"Entity is directly connected to {centrality[top_entity_id]} other entities in the network.",
                    evidence=[] # Calculated insight, relies on node
                ))
                
        # Find paths between key entities (e.g. across cases)
        # For simplicity, we just expose the pathfinding method to be used by the CorrelationEngine
        
        return insights
        
    def _calculate_degree_centrality(self, entities: List[Entity]) -> Dict[str, int]:
        centrality = {}
        for ent in entities:
            neighbors = self.relationship_engine.get_neighbors(ent.id)
            centrality[ent.id] = len(neighbors)
        return centrality

    def find_shortest_path(self, start_entity_id: str, end_entity_id: str, max_depth: int = 3) -> Optional[Tuple[List[str], List[str]]]:
        """
        Finds shortest path between two entities using only existing source edges.
        Returns Tuple(path_node_ids, evidence_source_record_ids).
        """
        if start_entity_id == end_entity_id:
            return None
            
        queue = deque([(start_entity_id, [start_entity_id], [])])
        visited = {start_entity_id}
        
        while queue:
            current_id, path, evidence = queue.popleft()
            
            if len(path) > max_depth + 1:
                continue
                
            neighbors = self.relationship_engine.get_neighbors(current_id)
            for rel in neighbors:
                next_id = rel.target if rel.source == current_id else rel.source
                
                if next_id == end_entity_id:
                    new_path = path + [next_id]
                    # Only collect actual source records, skip RESOLUTION_ENGINE
                    new_evidence = evidence + ([rel.sourceRecord] if rel.sourceRecord != "RESOLUTION_ENGINE" else [])
                    return new_path, list(set(new_evidence))
                    
                if next_id not in visited:
                    visited.add(next_id)
                    new_path = path + [next_id]
                    new_evidence = evidence + ([rel.sourceRecord] if rel.sourceRecord != "RESOLUTION_ENGINE" else [])
                    queue.append((next_id, new_path, new_evidence))
                    
        return None
