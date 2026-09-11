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

    def generate_timeline_events(self, raw_records: list) -> List[TimelineEvent]:
        events = []
        relations = self.relationship_engine.get_relations()
        
        record_to_entities = {}
        for r in relations:
            if r.sourceRecord and r.sourceRecord != "RESOLUTION_ENGINE":
                if r.sourceRecord not in record_to_entities:
                    record_to_entities[r.sourceRecord] = set()
                record_to_entities[r.sourceRecord].add(r.source)
                record_to_entities[r.sourceRecord].add(r.target)
                
        seen_ids = set()
                
        for rec in raw_records:
            record_id = rec.get("record_id")
            record_type = rec.get("record_type")
            ts = rec.get("timestamp")
            
            if not record_id or not record_type or not ts:
                continue
                
            event_id = f"TL-{record_id}"
            if event_id in seen_ids:
                continue
            seen_ids.add(event_id)
                
            try:
                dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                date_str = dt.strftime("%Y-%m-%d %H:%M")
                day_str = dt.strftime("%b %d, %Y")
            except:
                date_str = ts
                day_str = ts

            category = "communication"
            title = "Activity"
            detail = ""
            
            if record_type == "call_record":
                category = "communication"
                title = "Communication Event"
            elif record_type == "vehicle_sighting":
                category = "vehicle"
                title = "Vehicle Sighting"
            elif record_type == "financial_transaction":
                category = "financial"
                title = "Financial Transaction"
            elif record_type == "case_report":
                category = "case"
                title = "Case Report"
                
            struct_data = rec.get("structured_data", {})
            text_content = rec.get("text_content", "")
            
            if record_type == "call_record":
                caller = struct_data.get("caller", "")
                receiver = struct_data.get("receiver", "")
                if caller and receiver:
                    detail = f"Call from {caller} to {receiver}."
                else:
                    detail = text_content
            elif record_type == "vehicle_sighting":
                plate = struct_data.get("plate", "")
                loc = struct_data.get("location", "")
                if plate and loc:
                    detail = f"Vehicle {plate} observed at {loc}."
                else:
                    detail = text_content
            elif record_type == "financial_transaction":
                sender = struct_data.get("sender", "")
                receiver = struct_data.get("receiver", "")
                amount = struct_data.get("amount", "")
                if sender and receiver:
                    detail = f"Transfer of {amount} from {sender} to {receiver}."
                else:
                    detail = text_content
            elif record_type == "case_report":
                detail = text_content
                
            if not detail:
                detail = f"Record of type {record_type} logged at {day_str}."
                
            event_entities = list(record_to_entities.get(record_id, set()))
            
            events.append(TimelineEvent(
                id=event_id,
                date=date_str,
                day=day_str,
                category=category,
                title=title,
                detail=detail,
                entities=event_entities,
                record=record_id
            ))
            
        events.sort(key=lambda x: x.date, reverse=True)
        return events
