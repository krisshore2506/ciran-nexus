from typing import List, Dict, Any
from models.domain import EvidenceItem, EvidenceSource, EvidenceAudit
import datetime

class EvidenceEngine:
    def __init__(self):
        self.evidence_store: List[EvidenceItem] = []
        
    def register_evidence(self, insight: str, source_ids: List[str], analysis: str, relationship: str, raw_records: List[Dict[str, Any]]) -> EvidenceItem:
        
        sources = []
        for sid in source_ids:
            # Find the record to get metadata
            record = next((r for r in raw_records if r["record_id"] == sid), None)
            timestamp = record["timestamp"] if record else datetime.datetime.now().isoformat()
            rtype = record["record_type"] if record else "Unknown"
            
            sources.append(EvidenceSource(
                id=sid,
                type=rtype,
                timestamp=timestamp
            ))
            
        evidence_id = f"EV-{len(self.evidence_store) + 1}"
        
        item = EvidenceItem(
            id=evidence_id,
            insight=insight,
            sources=sources,
            analysis=analysis,
            relationship=relationship,
            status="Pending Analyst Review",
            audit=[
                EvidenceAudit(
                    stage="Detected",
                    actor="CIRAN Intelligence Engine (Phase 1)",
                    timestamp=datetime.datetime.now().isoformat(),
                    note="Generated automatically via rule-based inference."
                )
            ]
        )
        
        self.evidence_store.append(item)
        return item
        
    def get_all_evidence(self) -> List[EvidenceItem]:
        return self.evidence_store
