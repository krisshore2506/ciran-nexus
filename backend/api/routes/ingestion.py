from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from api.state import state
from ingestion.loaders import load_json
from ingestion.normalizer import normalize_records
from ingestion.adapters import get_adapter

router = APIRouter()

class IngestionRequest(BaseModel):
    dataset: Optional[str] = None
    file_path: Optional[str] = None
    max_rows: Optional[int] = None


@router.post("/load")
def load_data(req: Optional[IngestionRequest] = None):
    # Phase 1 Legacy support for zero frontend modification
    if not req or not req.dataset:
        raw_records = load_json("data/sample/synthetic_data.json")
        normalized = normalize_records(raw_records)
        
        # Process through pipeline
        for rec in normalized:
            extracted = state.entity_service.process_record(rec)
            state.relationship_engine.process_record(rec, extracted)
            
        return _run_post_ingestion_pipeline(len(raw_records), normalized)
        
    # Phase 2 Unified Integration Flow
    adapter = get_adapter(req.dataset, req.file_path)
    
    record_metadata = []
    
    records_processed = 0
    for source_record in adapter.stream_records(max_rows=req.max_rows):
        # Cache minimal metadata for evidence engine
        record_metadata.append({
            "record_id": source_record.source_record_id,
            "record_type": source_record.record_type,
            "timestamp": source_record.timestamp
        })
        
        # 1. Add unified entities to the state
        extracted_entities = state.entity_service.process_unified_entities(source_record.entities)
        
        # 2. Add unified relationships to the state
        state.relationship_engine.process_unified_relationships(source_record.relationships)
        
        records_processed += 1
        
    res = _run_post_ingestion_pipeline(records_processed, record_metadata)
    res["adapter_validation"] = {
        "accepted": adapter.validation_result.accepted,
        "rejected": adapter.validation_result.rejected
    }
    res["dataset"] = req.dataset
    return res

def _run_post_ingestion_pipeline(records_processed: int, raw_records: list):
    # Update global state entities and relations
    state.entities = list(state.entity_service.entities_store.values())
    state.relations = state.relationship_engine.get_relations()

    # Phase 3: Entity Resolution (generate SAME_AS/POSSIBLE_MATCH edges)
    state.entity_resolution_service.process_entities(state.entities)
    
    # Update global relation state after resolution
    state.relations = state.relationship_engine.get_relations()

    # Phase 3: Temporal and Graph Insights
    temp_insights = state.temporal_analysis.generate_insights(state.entities)
    state.timeline = state.temporal_analysis.generate_timeline_events(raw_records)
    graph_insights = state.graph_intelligence.generate_insights(state.entities)
    state.patterns.extend(temp_insights)
    state.patterns.extend(graph_insights)
    
    # Run risk engine
    for ent in state.entities:
        state.risk_engine.calculate_entity_priority(ent)
        
    state.alerts = state.risk_engine.generate_alerts(state.entities)
    
    # Phase 1/3: Correlate Cases (Multi-hop enabled)
    new_links = state.correlation_engine.find_cross_case_links(state.entities)
    state.cross_case_links = [res[0] for res in new_links]
    
    # Register evidence for cross case links
    for link, source_ids in new_links:
        ev = state.evidence_engine.register_evidence(
            insight=link.summary,
            source_ids=source_ids,
            analysis="Cross-case correlation detected via shared entities",
            relationship="Shared attributes",
            raw_records=raw_records
        )
        link.evidence = [ev.id]
        
    state.evidence = state.evidence_engine.get_all_evidence()
    
    return {
        "status": "success", 
        "message": "Data ingested and analyzed",
        "stats": {
            "records_processed": records_processed,
            "entities_extracted": len(state.entities),
            "relationships_created": len(state.relations),
            "alerts_generated": len(state.alerts),
            "cross_case_links": len(state.cross_case_links)
        }
    }
    

