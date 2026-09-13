import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.sql_models import Entity as SQLEntity

class IdentityResolver:
    @staticmethod
    def _generate_id(entity_type: str, value: str) -> str:
        # Predictable ID generation for synthetic data parity
        prefix_map = {
            "person": "P",
            "phone": "PH",
            "vehicle": "V",
            "account": "AC",
            "location": "L",
            "case": "CASE"
        }
        prefix = prefix_map.get(entity_type.lower(), "E")
        
        if entity_type.lower() == "person":
            parts = value.split()
            if parts:
                return f"{prefix}-{parts[0].upper()}"
        elif entity_type.lower() == "phone" and len(value) >= 4:
            return f"{prefix}-{value[-4:]}"
        elif entity_type.lower() == "vehicle" and len(value) >= 4:
            return f"{prefix}-{value[-4:]}"
        elif entity_type.lower() == "account" and len(value) >= 3:
            return f"{prefix}-{value[-3:]}"
        elif entity_type.lower() == "location" and len(value) >= 1:
            return f"{prefix}-{value[-1]}"
        elif entity_type.lower() == "case":
            return value.upper()
            
        return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"

    @staticmethod
    def resolve_entity(label: str, entity_type: str, db: Session) -> str:
        """
        Resolves an entity to an existing ID or generates a new one.
        Follows strict identity resolution to avoid false merges.
        """
        label_norm = label.strip()
        type_norm = entity_type.strip().lower()
        
        # Priority: Exact normalized identifier match
        existing = db.query(SQLEntity).filter(
            func.lower(SQLEntity.label) == label_norm.lower(),
            SQLEntity.type == type_norm
        ).first()
        
        if existing:
            return existing.id
            
        # If no strict match, generate new ID
        return IdentityResolver._generate_id(type_norm, label_norm)
