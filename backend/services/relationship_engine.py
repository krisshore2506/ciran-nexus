from typing import List, Dict, Any, Optional
from models.domain import Relation, Entity

class RelationshipEngine:
    def __init__(self):
        self.relations: List[Relation] = []
        # adjacency list for graph traversal
        self.graph: Dict[str, List[Relation]] = {}
        
    def add_relation(self, source: str, target: str, rel_type: str, label: str, confidence: int, record_id: str, timestamp: Optional[str] = None):
        if source == target:
            return
            
        rel = Relation(
            source=source,
            target=target,
            type=rel_type, # type: ignore
            label=label,
            confidence=confidence,
            sourceRecord=record_id,
            timestamp=timestamp
        )
        self.relations.append(rel)
        
        if source not in self.graph:
            self.graph[source] = []
        self.graph[source].append(rel)
        
        if target not in self.graph:
            self.graph[target] = []
        self.graph[target].append(rel)

    def process_record(self, record: Dict[str, Any], extracted_entities: List[Entity]):
        """
        Creates edges between entities co-occurring in a single record.
        """
        record_id = record["record_id"]
        rec_type = record["record_type"]
        
        # Build logic based on record type
        if rec_type == "call_record":
            phones = [e for e in extracted_entities if e.type == "phone"]
            persons = [e for e in extracted_entities if e.type == "person"]
            # Connect phones to each other
            if len(phones) >= 2:
                self.add_relation(phones[0].id, phones[1].id, "communication", "Call logged", 95, record_id)
            # Connect persons to their phones if possible, or all persons to phones
            for p in persons:
                for ph in phones:
                    self.add_relation(p.id, ph.id, "communication", "Subscriber association", 80, record_id)
                    
        elif rec_type == "vehicle_sighting":
            vehicles = [e for e in extracted_entities if e.type == "vehicle"]
            persons = [e for e in extracted_entities if e.type == "person"]
            locations = [e for e in extracted_entities if e.type == "location"]
            
            for v in vehicles:
                for p in persons:
                    self.add_relation(p.id, v.id, "vehicle", "Vehicle usage recorded", 85, record_id)
                for l in locations:
                    self.add_relation(v.id, l.id, "location", "Vehicle sighting", 90, record_id)
                    
        elif rec_type == "financial_transaction":
            accounts = [e for e in extracted_entities if e.type == "account"]
            if len(accounts) >= 2:
                self.add_relation(accounts[0].id, accounts[1].id, "financial", "Transfer detected", 90, record_id)
            persons = [e for e in extracted_entities if e.type == "person"]
            for p in persons:
                for a in accounts:
                    self.add_relation(p.id, a.id, "financial", "Account association", 80, record_id)
                    
        elif rec_type == "case_report":
            cases = [e for e in extracted_entities if e.type == "case"]
            other_ents = [e for e in extracted_entities if e.type != "case"]
            
            for c in cases:
                for o in other_ents:
                    self.add_relation(o.id, c.id, "case", "Named in record", 99, record_id)

    def get_relations(self) -> List[Relation]:
        return self.relations
        
    def get_neighbors(self, entity_id: str) -> List[Relation]:
        return self.graph.get(entity_id, [])

    def process_unified_relationships(self, unified_relationships: List[Any]):
        """
        Registers explicitly defined relationships from the Unified Model adapters
        """
        for u_rel in unified_relationships:
            # Join multiple source records into a single string for legacy compatibility 
            # or just take the first. The evidence engine uses it to lookup.
            rec_id = u_rel.source_record_ids[0] if u_rel.source_record_ids else "Unknown"
            
            # Map UnifiedRelationshipType to frontend RelationType if necessary
            # e.g., COMMUNICATION -> communication, TRANSACTION -> financial
            rel_type_map = {
                "COMMUNICATION": "communication",
                "TRANSACTION": "financial",
                "INVOLVED_IN": "case",
                "LOCATED_AT": "location",
                "ASSOCIATED_WITH": "organization",
                "OCCURRED_AT": "location"
            }
            
            mapped_type = rel_type_map.get(u_rel.relationship_type, "case")
            
            # The label should ideally describe the relationship based on attributes or type
            label = u_rel.relationship_type.replace("_", " ").capitalize()
            if "type" in u_rel.attributes:
                label = str(u_rel.attributes["type"]).capitalize()
                
            self.add_relation(
                source=u_rel.source_entity,
                target=u_rel.target_entity,
                rel_type=mapped_type,
                label=label,
                confidence=int(u_rel.confidence * 100),
                record_id=rec_id,
                timestamp=u_rel.timestamp
            )
