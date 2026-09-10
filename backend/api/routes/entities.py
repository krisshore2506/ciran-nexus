from fastapi import APIRouter, HTTPException
from typing import List, Optional
from api.state import state
from models.domain import Entity

router = APIRouter()

@router.get("", response_model=List[Entity])
def get_entities(q: Optional[str] = None):
    if not q:
        return state.entities
    
    q_lower = q.lower()
    results = []
    for e in state.entities:
        if q_lower in e.label.lower() or (e.subtitle and q_lower in e.subtitle.lower()) or q_lower in e.id.lower():
            results.append(e)
            
    # Limit to top 8 matches for performance
    return results[:8]

@router.get("/{id}", response_model=Entity)
def get_entity(id: str):
    for e in state.entities:
        if e.id == id:
            return e
    raise HTTPException(status_code=404, detail="Entity not found")

@router.get("/{id}/network")
def get_entity_network(id: str):
    entity = get_entity(id)
    edges = state.relationship_engine.get_neighbors(id)
    
    node_ids = set([id])
    for e in edges:
        node_ids.add(e.source)
        node_ids.add(e.target)
        
    nodes = [e for e in state.entities if e.id in node_ids]
    
    return {
        "nodes": nodes,
        "edges": edges
    }

@router.get("/{id}/timeline")
def get_entity_timeline(id: str):
    return [t for t in state.timeline if id in t.entities]
