from fastapi import APIRouter, Depends
from config.neo4j import get_neo4j
from config.db import get_db
from sqlalchemy.orm import Session
from models.sql_models import Entity as SQLEntity

router = APIRouter()

@router.get("")
def get_network(db: Session = Depends(get_db), neo4j_session = Depends(get_neo4j)):
    # Fetch all nodes from PostgreSQL
    nodes = db.query(SQLEntity).all()
    
    # Fetch all relationships from Neo4j
    result = neo4j_session.run("""
        MATCH (source)-[r]->(target)
        RETURN source.id AS source, 
               target.id AS target, 
               type(r) AS type,
               r.label AS label,
               r.confidence AS confidence,
               r.sourceRecord AS sourceRecord,
               r.timestamp AS timestamp
    """)
    
    edges = []
    for record in result:
        edges.append({
            "source": record["source"],
            "target": record["target"],
            "type": record["type"].lower(), # map back to domain enum if needed
            "label": record.get("label", ""),
            "confidence": record.get("confidence", 100),
            "sourceRecord": record.get("sourceRecord", ""),
            "timestamp": record.get("timestamp")
        })
        
    return {
        "nodes": nodes,
        "edges": edges
    }
