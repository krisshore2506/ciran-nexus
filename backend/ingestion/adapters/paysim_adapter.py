import csv
import uuid
from typing import Iterator
from models.unified import SourceRecord, UnifiedEntity, UnifiedRelationship, Provenance
from ingestion.adapters.base_adapter import BaseAdapter
from ingestion.validators import validate_row, validate_numeric
from ingestion.resolution import generate_entity_id, generate_relationship_id

class PaySimAdapter(BaseAdapter):
    def stream_records(self, max_rows: int = None) -> Iterator[SourceRecord]:
        count = 0
        with open(self.file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if max_rows and count >= max_rows:
                    break
                
                if not validate_row(row, ["step", "type", "amount", "nameOrig", "nameDest"]):
                    self.validation_result.rejected += 1
                    continue
                
                self.validation_result.accepted += 1
                count += 1
                
                rec_id = f"PAYSIM-{uuid.uuid4().hex[:8].upper()}"
                
                src_id = str(row["nameOrig"])
                dest_id = str(row["nameDest"])
                step = str(row["step"])
                
                src_ent = UnifiedEntity(
                    entity_id=generate_entity_id("PAYSIM", src_id),
                    entity_type="ACCOUNT",
                    label=src_id,
                    identifiers={"account_id": src_id},
                    attributes={
                        "old_balance": float(row["oldbalanceOrg"]) if validate_numeric(row.get("oldbalanceOrg")) else None,
                        "new_balance": float(row["newbalanceOrig"]) if validate_numeric(row.get("newbalanceOrig")) else None
                    }
                )
                
                dest_ent = UnifiedEntity(
                    entity_id=generate_entity_id("PAYSIM", dest_id),
                    entity_type="ACCOUNT",
                    label=dest_id,
                    identifiers={"account_id": dest_id},
                    attributes={
                        "old_balance": float(row["oldbalanceDest"]) if validate_numeric(row.get("oldbalanceDest")) else None,
                        "new_balance": float(row["newbalanceDest"]) if validate_numeric(row.get("newbalanceDest")) else None
                    }
                )
                
                rel = UnifiedRelationship(
                    relationship_id=generate_relationship_id(src_ent.entity_id, dest_ent.entity_id, "TRANSACTION", step),
                    source_entity=src_ent.entity_id,
                    target_entity=dest_ent.entity_id,
                    relationship_type="TRANSACTION",
                    timestamp=step, # Preserving simulation step, not fabricating timestamp
                    attributes={
                        "type": row.get("type", ""),
                        "amount": float(row["amount"]) if validate_numeric(row.get("amount")) else None,
                        "is_fraud": row.get("isFraud", "0") == "1",
                        "is_flagged_fraud": row.get("isFlaggedFraud", "0") == "1"
                    },
                    source_record_ids=[rec_id]
                )
                
                provenance = Provenance(
                    source_dataset="paysim",
                    source_file=self.file_path,
                    source_record_id=rec_id
                )
                
                yield SourceRecord(
                    source_record_id=rec_id,
                    source_dataset="paysim",
                    record_type="financial_transaction",
                    timestamp=step,
                    entities=[src_ent, dest_ent],
                    relationships=[rel],
                    provenance=provenance
                )
