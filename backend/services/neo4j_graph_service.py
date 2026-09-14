import os
from typing import List, Dict, Any, Optional, Tuple
from neo4j import Session
from models.domain import Entity

class Neo4jGraphService:
    def __init__(self, session: Session):
        self.session = session
        # As per Phase 1, Neo4j nodes were created with labels like Person, Phone, Vehicle, Account, Location, Case
        self.labels = ["Person", "Phone", "Vehicle", "Account", "Location", "Case"]

    def create_constraints(self):
        """
        Creates unique constraints for all known entity labels based on 'id'.
        Uses APOC or basic Cypher constraints depending on neo4j version. 
        Neo4j 4.x/5.x syntax is `CREATE CONSTRAINT ... FOR (n:Label) REQUIRE n.id IS UNIQUE`
        """
        for label in self.labels:
            query = f"CREATE CONSTRAINT IF NOT EXISTS FOR (n:{label}) REQUIRE n.id IS UNIQUE"
            try:
                self.session.run(query)
            except Exception as e:
                # Might already exist or syntax difference
                print(f"Warning creating constraint for {label}: {e}")

    def get_direct_neighbors(self, entity_id: str) -> Dict[str, Any]:
        """
        Returns nodes and edges directly connected to entity_id.
        """
        query = """
        MATCH (source {id: $entity_id})-[r]-(target)
        RETURN target.id AS target_id, target.label AS target_label, labels(target) AS target_labels,
               type(r) AS rel_type, r.label AS rel_label, r.confidence AS confidence, 
               r.sourceRecord AS sourceRecord, r.timestamp AS timestamp
        """
        result = self.session.run(query, entity_id=entity_id)
        
        nodes = []
        relationships = []
        seen_nodes = set()
        
        for record in result:
            tgt_id = record["target_id"]
            if tgt_id not in seen_nodes:
                nodes.append({
                    "id": tgt_id,
                    "label": record["target_label"],
                    "labels": record["target_labels"]
                })
                seen_nodes.add(tgt_id)
                
            relationships.append({
                "source": entity_id,
                "target": tgt_id,
                "type": record["rel_type"].lower(),
                "label": record["rel_label"],
                "confidence": record["confidence"],
                "sourceRecord": record["sourceRecord"],
                "timestamp": record["timestamp"]
            })
            
        return {
            "nodes": nodes,
            "relationships": relationships
        }

    def get_multi_hop_network(self, entity_id: str, max_depth: int = 3) -> Dict[str, Any]:
        """
        Bounded multi-hop network traversal up to max_depth.
        max_depth is validated to be between 1 and 5.
        """
        if not (1 <= max_depth <= 5):
            max_depth = 3
            
        query = f"""
        MATCH path = (source {{id: $entity_id}})-[*1..{max_depth}]-(target)
        UNWIND nodes(path) AS n
        UNWIND relationships(path) AS r
        RETURN DISTINCT n.id AS n_id, n.label AS n_label, labels(n) AS n_labels,
                        startNode(r).id AS start_id, endNode(r).id AS end_id,
                        type(r) AS rel_type, r.label AS rel_label, r.confidence AS confidence, 
                        r.sourceRecord AS sourceRecord, r.timestamp AS timestamp
        LIMIT 1000
        """
        result = self.session.run(query, entity_id=entity_id)
        
        nodes_map = {}
        relationships_map = {}
        
        for record in result:
            n_id = record["n_id"]
            if n_id and n_id not in nodes_map:
                nodes_map[n_id] = {
                    "id": n_id,
                    "label": record["n_label"],
                    "labels": record["n_labels"]
                }
                
            rel_id = f"{record['start_id']}-{record['end_id']}-{record['rel_type']}"
            if record["start_id"] and record["end_id"] and rel_id not in relationships_map:
                relationships_map[rel_id] = {
                    "source": record["start_id"],
                    "target": record["end_id"],
                    "type": record["rel_type"].lower(),
                    "label": record["rel_label"],
                    "confidence": record["confidence"],
                    "sourceRecord": record["sourceRecord"],
                    "timestamp": record["timestamp"]
                }
                
        return {
            "nodes": list(nodes_map.values()),
            "relationships": list(relationships_map.values())
        }

    def find_shortest_path(self, source_id: str, target_id: str, max_depth: int = 4) -> Optional[Dict[str, Any]]:
        """
        Finds shortest path between two nodes using Neo4j shortestPath.
        """
        if source_id == target_id:
            return None
            
        if not (1 <= max_depth <= 6):
            max_depth = 4
            
        query = f"""
        MATCH path = shortestPath((a {{id: $source_id}})-[*..{max_depth}]-(b {{id: $target_id}}))
        RETURN path, length(path) AS path_length
        """
        result = self.session.run(query, source_id=source_id, target_id=target_id).single()
        
        if not result:
            return None
            
        path = result["path"]
        path_length = result["path_length"]
        
        nodes = []
        for n in path.nodes:
            nodes.append({
                "id": n["id"],
                "label": n["label"],
                "labels": list(n.labels)
            })
            
        relationships = []
        for r in path.relationships:
            relationships.append({
                "source": r.nodes[0]["id"],
                "target": r.nodes[1]["id"],
                "type": r.type.lower(),
                "label": r.get("label"),
                "confidence": r.get("confidence"),
                "sourceRecord": r.get("sourceRecord"),
                "timestamp": r.get("timestamp")
            })
            
        node_ids = [n["id"] for n in nodes]
        
        return {
            "source": source_id,
            "target": target_id,
            "path": node_ids,
            "nodes": nodes,
            "relationships": relationships,
            "path_length": path_length
        }

    def get_common_connections(self, entity_a_id: str, entity_b_id: str) -> List[Dict[str, Any]]:
        """
        Finds meaningful shared neighboring entities between A and B.
        """
        if entity_a_id == entity_b_id:
            return []
            
        query = """
        MATCH (a {id: $entity_a})-[r1]-(common)-[r2]-(b {id: $entity_b})
        RETURN DISTINCT common.id AS common_id, common.label AS common_label, labels(common) AS common_labels,
                        type(r1) AS r1_type, r1.label AS r1_label, r1.sourceRecord AS r1_record,
                        type(r2) AS r2_type, r2.label AS r2_label, r2.sourceRecord AS r2_record
        LIMIT 50
        """
        result = self.session.run(query, entity_a=entity_a_id, entity_b=entity_b_id)
        
        common_nodes = []
        for record in result:
            common_nodes.append({
                "common_entity": {
                    "id": record["common_id"],
                    "label": record["common_label"],
                    "labels": record["common_labels"]
                },
                "relationship_context": {
                    "to_a": {
                        "type": record["r1_type"].lower(),
                        "label": record["r1_label"],
                        "sourceRecord": record["r1_record"]
                    },
                    "to_b": {
                        "type": record["r2_type"].lower(),
                        "label": record["r2_label"],
                        "sourceRecord": record["r2_record"]
                    }
                }
            })
            
        return common_nodes

    def get_case_network(self, case_id: str) -> Dict[str, Any]:
        """
        Returns the immediate network (depth 1) for a specific case.
        """
        # Case network is effectively just direct neighbors, but we ensure the center is a Case
        query = """
        MATCH (c:Case {id: $case_id})-[r]-(target)
        RETURN target.id AS target_id, target.label AS target_label, labels(target) AS target_labels,
               type(r) AS rel_type, r.label AS rel_label, r.confidence AS confidence, 
               r.sourceRecord AS sourceRecord, r.timestamp AS timestamp
        LIMIT 200
        """
        result = self.session.run(query, case_id=case_id)
        
        nodes = [{"id": case_id, "label": case_id, "labels": ["Case"]}] # Ensure root is there
        relationships = []
        seen_nodes = set([case_id])
        
        for record in result:
            tgt_id = record["target_id"]
            if tgt_id not in seen_nodes:
                nodes.append({
                    "id": tgt_id,
                    "label": record["target_label"],
                    "labels": record["target_labels"]
                })
                seen_nodes.add(tgt_id)
                
            relationships.append({
                "source": case_id,
                "target": tgt_id,
                "type": record["rel_type"].lower(),
                "label": record["rel_label"],
                "confidence": record["confidence"],
                "sourceRecord": record["sourceRecord"],
                "timestamp": record["timestamp"]
            })
            
        return {
            "nodes": nodes,
            "relationships": relationships
        }

    def get_graph_metrics(self, entity_id: str) -> Dict[str, Any]:
        """
        Simple, explainable metrics: direct connection count (degree) and related case count.
        """
        query = """
        MATCH (n {id: $entity_id})-[r]-(m)
        RETURN count(DISTINCT m) AS degree,
               sum(CASE WHEN 'Case' IN labels(m) THEN 1 ELSE 0 END) AS case_count
        """
        result = self.session.run(query, entity_id=entity_id).single()
        
        if not result:
            return {"degree": 0, "case_count": 0}
            
        return {
            "degree": result["degree"],
            "case_count": result["case_count"]
        }
