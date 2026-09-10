from typing import List, Dict, Optional
import uuid
from models.domain import Entity, Relation
from services.relationship_engine import RelationshipEngine

class EntityResolutionService:
    def __init__(self, relationship_engine: RelationshipEngine):
        self.relationship_engine = relationship_engine
        
    def process_entities(self, entities: List[Entity]):
        """
        Conservative Entity Resolution. 
        Only creates SAME_AS edges for strictly deterministic identical identifiers 
        across different namespaces, or POSSIBLE_MATCH for weaker similarities.
        """
        # Group entities by type
        by_type: Dict[str, List[Entity]] = {}
        for ent in entities:
            if ent.type not in by_type:
                by_type[ent.type] = []
            by_type[ent.type].append(ent)
            
        # Process deterministic matches
        self._resolve_phones(by_type.get("phone", []))
        self._resolve_accounts(by_type.get("account", []))
        
    def _get_namespace(self, entity_id: str) -> str:
        return entity_id.split("-")[0] if "-" in entity_id else "UNKNOWN"
        
    def _create_match_edge(self, source: Entity, target: Entity, match_type: str, confidence: int, reason: str):
        # Prevent self-match or intra-dataset merge for resolution
        if self._get_namespace(source.id) == self._get_namespace(target.id):
            return
            
        rel_id = f"RES-{uuid.uuid4().hex[:8].upper()}"
        rel = Relation(
            source=source.id,
            target=target.id,
            type=match_type, # SAME_AS or POSSIBLE_MATCH
            label=reason,
            confidence=confidence,
            sourceRecord="RESOLUTION_ENGINE" # explicitly mark as derived/inferred
        )
        self.relationship_engine.add_relation(
            source=rel.source,
            target=rel.target,
            rel_type=rel.type,
            label=rel.label,
            confidence=rel.confidence,
            record_id=rel.sourceRecord
        )

    def _resolve_phones(self, phones: List[Entity]):
        # Deterministic match: Exact same phone number
        for i, p1 in enumerate(phones):
            for p2 in phones[i+1:]:
                # We expect the label or specific attribute to hold the phone number
                num1 = self._extract_identifier(p1, "phone_number") or p1.label.replace("Phone ", "")
                num2 = self._extract_identifier(p2, "phone_number") or p2.label.replace("Phone ", "")
                
                if num1 and num2 and num1 == num2 and num1.strip() != "":
                    self._create_match_edge(p1, p2, "SAME_AS", 100, f"Deterministic match: identical phone number {num1}")

    def _resolve_accounts(self, accounts: List[Entity]):
        for i, a1 in enumerate(accounts):
            for a2 in accounts[i+1:]:
                # Example: Explicit identifier match
                id1 = self._extract_identifier(a1, "email_id") or self._extract_identifier(a1, "account_id")
                id2 = self._extract_identifier(a2, "email_id") or self._extract_identifier(a2, "account_id")
                
                if id1 and id2 and id1 == id2 and id1.strip() != "":
                    self._create_match_edge(a1, a2, "SAME_AS", 100, f"Deterministic match: identical account ID {id1}")

    def _extract_identifier(self, entity: Entity, key: str) -> Optional[str]:
        if not entity.attributes:
            return None
        for attr in entity.attributes:
            if attr.label == key:
                return attr.value
        return None
