import csv
from typing import Iterator, Dict
from models.unified import SourceRecord, UnifiedEntity, UnifiedRelationship, Provenance, Location
from ingestion.adapters.base_adapter import BaseAdapter
from ingestion.validators import validate_row
from ingestion.resolution import generate_entity_id, generate_relationship_id

class CrimeAdapter(BaseAdapter):
    def stream_records(self, max_rows: int = None) -> Iterator[SourceRecord]:
        count = 0
        with open(self.file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if max_rows and count >= max_rows:
                    break
                
                # Validation
                if not validate_row(row, ["Report Number"]):
                    self.validation_result.rejected += 1
                    continue
                
                self.validation_result.accepted += 1
                count += 1
                
                rec_id = str(row["Report Number"])
                
                # Case Entity
                case_ent = UnifiedEntity(
                    entity_id=generate_entity_id("CRIME", rec_id),
                    entity_type="CASE",
                    label=f"Case {rec_id}",
                    identifiers={"report_number": rec_id},
                    attributes={
                        "crime_type": row.get("Crime Description", ""),
                        "crime_code": row.get("Crime Code", ""),
                        "crime_category": row.get("Crime Domain", ""),
                        "status": "Closed" if row.get("Case Closed") == "Yes" else "Open",
                        "victim_age": row.get("Victim Age", ""),
                        "victim_gender": row.get("Victim Gender", ""),
                        "weapon_used": row.get("Weapon Used", "")
                    }
                )
                
                entities = [case_ent]
                relationships = []
                
                # Location Entity
                city = row.get("City", "").strip()
                if city:
                    loc_ent = UnifiedEntity(
                        entity_id=generate_entity_id("LOC", city),
                        entity_type="LOCATION",
                        label=city,
                        identifiers={"city": city}
                    )
                    entities.append(loc_ent)
                    
                    relationships.append(UnifiedRelationship(
                        relationship_id=generate_relationship_id(case_ent.entity_id, loc_ent.entity_id, "OCCURRED_AT"),
                        source_entity=case_ent.entity_id,
                        target_entity=loc_ent.entity_id,
                        relationship_type="OCCURRED_AT",
                        source_record_ids=[rec_id]
                    ))
                
                # Combine Date and Time
                event_date = row.get("Date of Occurrence", "")
                event_time = row.get("Time of Occurrence", "")
                timestamp = f"{event_date}T{event_time}" if event_date and event_time else event_date
                
                provenance = Provenance(
                    source_dataset="crime",
                    source_file=self.file_path,
                    source_record_id=rec_id
                )
                
                yield SourceRecord(
                    source_record_id=rec_id,
                    source_dataset="crime",
                    record_type="case_report",
                    timestamp=timestamp,
                    entities=entities,
                    relationships=relationships,
                    provenance=provenance
                )
