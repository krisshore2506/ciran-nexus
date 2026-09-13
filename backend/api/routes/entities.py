from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from config.db import get_db
from config.neo4j import get_neo4j
from models.sql_models import Entity as SQLEntity, TimelineEvent as SQLTimelineEvent
from models.domain import Entity

router = APIRouter()

@router.get("", response_model=List[Entity])
def get_entities(q: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(SQLEntity)
    if q:
        q_lower = f"%{q.lower()}%"
        query = query.filter(
            or_(
                SQLEntity.label.ilike(q_lower),
                SQLEntity.subtitle.ilike(q_lower),
                SQLEntity.id.ilike(q_lower)
            )
        )
    return query.limit(8).all()

@router.get("/{id}", response_model=Entity)
def get_entity(id: str, db: Session = Depends(get_db)):
    entity = db.query(SQLEntity).filter(SQLEntity.id == id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity

@router.get("/{id}/network")
def get_entity_network(id: str, db: Session = Depends(get_db), neo4j_session = Depends(get_neo4j)):
    # Verify entity exists
    entity = get_entity(id, db)
    
    # Query Neo4j for 1-hop neighbors
    result = neo4j_session.run("""
        MATCH (n {id: $id})-[r]-(m)
        RETURN startNode(r).id AS source, 
               endNode(r).id AS target, 
               type(r) AS type,
               r.label AS label,
               r.confidence AS confidence,
               r.sourceRecord AS sourceRecord,
               r.timestamp AS timestamp,
               m.id AS neighbor_id
    """, id=id)
    
    edges = []
    neighbor_ids = set([id])
    for record in result:
        neighbor_ids.add(record["neighbor_id"])
        edges.append({
            "source": record["source"],
            "target": record["target"],
            "type": record["type"].lower(),
            "label": record.get("label", ""),
            "confidence": record.get("confidence", 100),
            "sourceRecord": record.get("sourceRecord", ""),
            "timestamp": record.get("timestamp")
        })
        
    # Fetch neighbor nodes from Postgres
    nodes = db.query(SQLEntity).filter(SQLEntity.id.in_(neighbor_ids)).all()
    
    return {
        "nodes": nodes,
        "edges": edges
    }

@router.get("/{id}/timeline")
def get_entity_timeline(id: str, db: Session = Depends(get_db)):
    # For Phase 1 we will still query timeline events from Postgres
    # using the Any mapping if timeline events exist in DB.
    # We will search if the id is in the entities array field.
    # Note: SQLite/Postgres specific array operations might differ.
    # We can fetch all and filter in python if array query is complex, 
    # but Postgres supports ANY().
    events = db.query(SQLTimelineEvent).filter(SQLTimelineEvent.entities.any(id)).all()
    return events
