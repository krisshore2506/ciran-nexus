from typing import List, Dict, Tuple, Optional
from models.domain import Entity, PatternInsight
from services.neo4j_graph_service import Neo4jGraphService
import uuid

class GraphIntelligenceService:
    def __init__(self, neo4j_service: Neo4jGraphService):
        self.neo4j_service = neo4j_service
        
    def generate_insights(self, entities: List[Entity]) -> List[PatternInsight]:
        insights = []
        
        # Calculate centrality using neo4j metrics
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
                
        return insights
        
    def _calculate_degree_centrality(self, entities: List[Entity]) -> Dict[str, int]:
        centrality = {}
        for ent in entities:
            if hasattr(self.neo4j_service, "get_graph_metrics"):
                metrics = self.neo4j_service.get_graph_metrics(ent.id)
                centrality[ent.id] = metrics.get("degree", 0)
            elif hasattr(self.neo4j_service, "get_relations"):
                # Fallback for legacy RelationshipEngine
                degree = sum(1 for r in self.neo4j_service.get_relations() if r.source == ent.id or r.target == ent.id)
                centrality[ent.id] = degree
        return centrality

    def find_shortest_path(self, start_entity_id: str, end_entity_id: str, max_depth: int = 3) -> Optional[Tuple[List[str], List[str]]]:
        """
        Finds shortest path between two entities using Neo4j shortestPath.
        Returns Tuple(path_node_ids, evidence_source_record_ids).
        """
        if not hasattr(self.neo4j_service, "find_shortest_path"):
            return None
        path_info = self.neo4j_service.find_shortest_path(start_entity_id, end_entity_id, max_depth)
        
        if not path_info:
            return None
            
        path_nodes = path_info["path"]
        evidence_sources = [r["sourceRecord"] for r in path_info["relationships"] if r.get("sourceRecord") and r.get("sourceRecord") != "RESOLUTION_ENGINE"]
        
        return path_nodes, list(set(evidence_sources))
