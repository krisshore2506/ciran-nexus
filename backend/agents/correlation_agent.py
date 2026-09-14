from ai.ciran_state import CIRANGraphState
from typing import Dict, Any
from services.neo4j_graph_service import Neo4jGraphService
from services.correlation_engine import CorrelationEngine
from services.relationship_engine import RelationshipEngine
from services.graph_intelligence import GraphIntelligenceService
from models.domain import Entity

class CorrelationAgent:
    def __init__(self, neo4j_graph: Neo4jGraphService):
        self.neo4j_graph = neo4j_graph
        self.graph_intel = GraphIntelligenceService(self.neo4j_graph)

    def execute(self, state: CIRANGraphState) -> CIRANGraphState:
        result = {
            "agent": "correlation",
            "status": "SUCCESS",
            "correlations": [],
            "supporting_evidence": [],
            "confidence": 0,
            "source_references": [],
            "errors": []
        }
        
        try:
            # 1. Extract exact entity IDs from context
            entity_ids = set()
            network_nodes = state.get("network_result", {}).get("nodes", [])
            for node in network_nodes:
                entity_ids.add(node["source_entity"]["id"])
                entity_ids.add(node["target_entity"]["id"])
                
            if not entity_ids:
                result["status"] = "NO_EVIDENCE"
                state["correlation_result"] = result
                return state

            # 2. Reconstruct localized RelationshipEngine environment for legacy engine
            rel_engine = RelationshipEngine()
            entities = []
            seen_entities = {}
            
            # Fetch base entities explicitly to ensure exact IDs and Labels
            query = "MATCH (n) WHERE n.id IN $ids RETURN n.id as id, n.label as label, labels(n) as labels"
            res = self.neo4j_graph.session.run(query, ids=list(entity_ids))
            for record in res:
                ent_type = record["labels"][0].lower() if record["labels"] else "unknown"
                if "Case" in record["labels"] or "CASE" in record["labels"]:
                    ent_type = "case"
                ent = Entity(id=record["id"], type=ent_type, label=record["label"], properties={})
                seen_entities[record["id"]] = ent
                entities.append(ent)
            
            for eid in entity_ids:
                # Fetch only exact deterministic neighborhood
                neighbors = self.neo4j_graph.get_direct_neighbors(eid)
                
                for rel in neighbors.get("relationships", []):
                    rel_engine.add_relation(
                        source=rel["source"],
                        target=rel["target"],
                        rel_type=rel["type"],
                        label=rel["label"],
                        confidence=rel.get("confidence", 50),
                        record_id=rel.get("sourceRecord", "UNKNOWN")
                    )
                
                for n in neighbors.get("nodes", []):
                    if n["id"] not in seen_entities:
                        ent_type = n["labels"][0].lower() if n["labels"] else "unknown"
                        if "Case" in n["labels"] or "CASE" in n["labels"]:
                            ent_type = "case"
                        ent = Entity(id=n["id"], type=ent_type, label=n["label"], properties={})
                        seen_entities[n["id"]] = ent
                        entities.append(ent)
            
            # 3. Delegate to Legacy CorrelationEngine safely
            engine = CorrelationEngine(rel_engine, self.graph_intel)
            links = engine.find_cross_case_links(entities)
            
            # 4. Map structured output
            for link, sources in links:
                result["correlations"].append({
                    "summary": link.summary,
                    "type": "Cross-Case Correlation",
                    "cases": link.cases,
                    "path": link.path
                })
                # Only trust valid sources
                valid_sources = [s for s in sources if s and s != "UNKNOWN" and s != "RESOLUTION_ENGINE"]
                result["supporting_evidence"].extend(valid_sources)
                result["source_references"].extend(valid_sources)
                result["confidence"] = max(result["confidence"], link.confidence)

            if not result["correlations"]:
                result["status"] = "NO_EVIDENCE"
            else:
                result["source_references"] = list(set(result["source_references"]))
                state["source_references"].extend(result["source_references"])

        except Exception as e:
            result["status"] = "ERROR"
            result["errors"].append(str(e))
            state["errors"].append(f"CorrelationAgent: {str(e)}")
            
        state["correlation_result"] = result
        return state
