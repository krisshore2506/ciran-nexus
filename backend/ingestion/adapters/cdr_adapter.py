import csv
import uuid
from typing import Iterator
from models.unified import SourceRecord, UnifiedEntity, UnifiedRelationship, Provenance, Location
from ingestion.adapters.base_adapter import BaseAdapter
from ingestion.validators import validate_row, validate_numeric
from ingestion.resolution import generate_entity_id, generate_relationship_id

class CDRAdapter(BaseAdapter):
    def stream_records(self, max_rows: int = None) -> Iterator[SourceRecord]:
        count = 0
        with open(self.file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if max_rows and count >= max_rows:
                    break
                
                if not validate_row(row, ["msisdn", "datetime", "cell_id"]):
                    self.validation_result.rejected += 1
                    continue
                
                self.validation_result.accepted += 1
                count += 1
                
                rec_id = f"CDR-{uuid.uuid4().hex[:8].upper()}"
                
                msisdn = str(row["msisdn"]).strip()
                timestamp = str(row["datetime"])
                cell_id = str(row["cell_id"]).strip()
                
                phone_ent = UnifiedEntity(
                    entity_id=generate_entity_id("CDR", msisdn),
                    entity_type="PHONE",
                    label=msisdn,
                    identifiers={"msisdn": msisdn},
                    attributes={
                        "service": row.get("service", "")
                    }
                )
                
                tower_ent = UnifiedEntity(
                    entity_id=generate_entity_id("CELL", cell_id),
                    entity_type="CELL_TOWER",
                    label=f"Tower {cell_id}",
                    identifiers={"cell_id": cell_id}
                )
                
                rel = UnifiedRelationship(
                    relationship_id=generate_relationship_id(phone_ent.entity_id, tower_ent.entity_id, "LOCATED_AT", timestamp),
                    source_entity=phone_ent.entity_id,
                    target_entity=tower_ent.entity_id,
                    relationship_type="LOCATED_AT",
                    timestamp=timestamp,
                    attributes={"data_type": row.get("data_type", "")},
                    source_record_ids=[rec_id]
                )
                
                lat, lon = None, None
                if validate_numeric(row.get("latitude")) and validate_numeric(row.get("longitude")):
                    lat = float(row["latitude"])
                    lon = float(row["longitude"])
                
                location = Location(
                    location_id=generate_entity_id("LOC", cell_id),
                    name=cell_id,
                    latitude=lat,
                    longitude=lon,
                    cell_id=cell_id
                ) if (lat is not None and lon is not None) else None
                
                provenance = Provenance(
                    source_dataset="itu_cdr",
                    source_file=self.file_path,
                    source_record_id=rec_id
                )
                
                yield SourceRecord(
                    source_record_id=rec_id,
                    source_dataset="itu_cdr",
                    record_type="cell_record",
                    timestamp=timestamp,
                    entities=[phone_ent, tower_ent],
                    relationships=[rel],
                    location=location,
                    attributes={"data_type": row.get("data_type", "")},
                    provenance=provenance
                )
