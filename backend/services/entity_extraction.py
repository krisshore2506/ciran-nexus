import uuid
from typing import List, Dict, Any
from models.domain import Entity, Attribute
from ai.nlp_service import extract_entities_from_text

class EntityExtractionService:
    def __init__(self):
        # In-memory store for deduplication across the dataset
        self.entities_store: Dict[str, Entity] = {}
        
    def _generate_id(self, entity_type: str, value: str) -> str:
        # Predictable ID generation for the synthetic data to match frontend expectations
        prefix_map = {
            "person": "P",
            "phone": "PH",
            "vehicle": "V",
            "account": "AC",
            "location": "L",
            "case": "CASE"
        }
        prefix = prefix_map.get(entity_type, "E")
        
        if entity_type == "person":
            return f"{prefix}-{value.split()[0].upper()}"
        elif entity_type == "phone":
            return f"{prefix}-{value[-4:]}"
        elif entity_type == "vehicle":
            return f"{prefix}-{value[-4:]}"
        elif entity_type == "account":
            return f"{prefix}-{value[-3:]}"
        elif entity_type == "location":
            return f"{prefix}-{value[-1]}"
        elif entity_type == "case":
            return value.upper()
        return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"

    def process_record(self, normalized_record: Dict[str, Any]) -> List[Entity]:
        extracted = []
        
        # Extract from structured data
        struct_data = normalized_record.get("structured_data", {})
        
        if normalized_record["record_type"] == "case_report":
            case_id = struct_data.get("case_id")
            if case_id:
                ent_id = self._generate_id("case", case_id)
                if ent_id not in self.entities_store:
                    self.entities_store[ent_id] = Entity(
                        id=ent_id,
                        type="case",
                        label=f"Case {case_id.split('-')[-1]}",
                        subtitle=f"{normalized_record['text_content'][:20]}...",
                        attributes=[Attribute(label="Entity Type", value="Case"), Attribute(label="Status", value=struct_data.get("status", "Unknown"))]
                    )
                extracted.append(self.entities_store[ent_id])
                
        # Use NLP for unstructured text
        text = normalized_record.get("text_content", "")
        nlp_ents = extract_entities_from_text(text)
        
        # Add explicit structured entities to NLP extraction to ensure they are captured
        if "caller" in struct_data: nlp_ents.append({"type": "phone", "value": struct_data["caller"]})
        if "receiver" in struct_data: nlp_ents.append({"type": "phone", "value": struct_data["receiver"]})
        if "name_a" in struct_data and struct_data["name_a"]: nlp_ents.append({"type": "person", "value": struct_data["name_a"]})
        if "name_b" in struct_data and struct_data["name_b"]: nlp_ents.append({"type": "person", "value": struct_data["name_b"]})
        if "plate" in struct_data: nlp_ents.append({"type": "vehicle", "value": struct_data["plate"]})
        if "location" in struct_data: nlp_ents.append({"type": "location", "value": struct_data["location"]})
        if "driver" in struct_data: nlp_ents.append({"type": "person", "value": struct_data["driver"]})
        if "sender" in struct_data: nlp_ents.append({"type": "account", "value": struct_data["sender"]})
        if "receiver_account" in struct_data: nlp_ents.append({"type": "account", "value": struct_data["receiver_account"]})

        # Deduplicate within record
        unique_ents = {f"{e['type']}:{e['value']}": e for e in nlp_ents}.values()

        for ent in unique_ents:
            ent_type = ent["type"]
            val = ent["value"]
            ent_id = self._generate_id(ent_type, val)
            
            if ent_id not in self.entities_store:
                self.entities_store[ent_id] = Entity(
                    id=ent_id,
                    type=ent_type, # type: ignore
                    label=val,
                    subtitle=f"{ent_type.capitalize()} record",
                    attributes=[Attribute(label="Entity Type", value=ent_type.capitalize())]
                )
            extracted.append(self.entities_store[ent_id])
            
        return extracted

    def process_unified_entities(self, unified_entities: List[Any]) -> List[Entity]:
        extracted = []
        for u_ent in unified_entities:
            ent_id = u_ent.entity_id
            if ent_id not in self.entities_store:
                attrs = [Attribute(label=k, value=str(v)) for k, v in u_ent.attributes.items() if v is not None]
                # Default subtitle to match frontend expectations
                subtitle = f"{u_ent.entity_type.capitalize()} record"
                if "status" in u_ent.attributes:
                    subtitle = f"Status: {u_ent.attributes['status']}"
                elif "service" in u_ent.attributes:
                    subtitle = f"Service: {u_ent.attributes['service']}"
                
                self.entities_store[ent_id] = Entity(
                    id=ent_id,
                    type=u_ent.entity_type.lower(), # Map UnifiedEntityType to frontend EntityType
                    label=u_ent.label,
                    subtitle=subtitle,
                    attributes=attrs
                )
            extracted.append(self.entities_store[ent_id])
        return extracted
