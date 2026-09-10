import csv
import uuid
import gzip
import os
from typing import Iterator, Dict
from models.unified import SourceRecord, UnifiedEntity, UnifiedRelationship, Provenance
from ingestion.adapters.base_adapter import BaseAdapter
from ingestion.validators import validate_row
from ingestion.resolution import generate_entity_id, generate_relationship_id

class EmailAdapter(BaseAdapter):
    def stream_records(self, max_rows: int = None) -> Iterator[SourceRecord]:
        count = 0
        is_gz = self.file_path.endswith('.gz')
        
        open_func = gzip.open if is_gz else open
        mode = 'rt' if is_gz else 'r'
        
        with open_func(self.file_path, mode, encoding="utf-8-sig") as f:
            if self.file_path.endswith('.csv'):
                reader = csv.DictReader(f)
                for row in reader:
                    if max_rows and count >= max_rows:
                        break
                    
                    if not validate_row(row, ["source", "destination", "timestamp"]):
                        self.validation_result.rejected += 1
                        continue
                    
                    yield self._process_row(row, count)
                    count += 1
            else:
                # Handle space-separated .txt or .txt.gz
                for line in f:
                    if max_rows and count >= max_rows:
                        break
                        
                    parts = line.strip().split()
                    if len(parts) < 3:
                        self.validation_result.rejected += 1
                        continue
                        
                    row = {
                        "source": parts[0],
                        "destination": parts[1],
                        "timestamp": parts[2]
                    }
                    
                    yield self._process_row(row, count)
                    count += 1

    def _process_row(self, row: Dict[str, str], count: int) -> SourceRecord:
        self.validation_result.accepted += 1
        
        rec_id = f"EMAIL-{uuid.uuid4().hex[:8].upper()}"
        
        source_id = str(row["source"])
        dest_id = str(row["destination"])
        timestamp = str(row["timestamp"])
        
        src_ent = UnifiedEntity(
            entity_id=generate_entity_id("EMAIL", source_id),
            entity_type="ACCOUNT",
            label=f"Email User {source_id}",
            identifiers={"email_id": source_id}
        )
        
        dest_ent = UnifiedEntity(
            entity_id=generate_entity_id("EMAIL", dest_id),
            entity_type="ACCOUNT",
            label=f"Email User {dest_id}",
            identifiers={"email_id": dest_id}
        )
        
        rel = UnifiedRelationship(
            relationship_id=generate_relationship_id(src_ent.entity_id, dest_ent.entity_id, "COMMUNICATION", timestamp),
            source_entity=src_ent.entity_id,
            target_entity=dest_ent.entity_id,
            relationship_type="COMMUNICATION",
            timestamp=timestamp,
            source_record_ids=[rec_id]
        )
        
        provenance = Provenance(
            source_dataset="email_eu_core",
            source_file=os.path.basename(self.file_path),
            source_record_id=rec_id
        )
        
        return SourceRecord(
            source_record_id=rec_id,
            source_dataset="email_eu_core",
            record_type="communication",
            timestamp=timestamp,
            entities=[src_ent, dest_ent],
            relationships=[rel],
            provenance=provenance
        )
