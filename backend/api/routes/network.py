from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from config.neo4j import get_neo4j
from services.neo4j_graph_service import Neo4jGraphService
from neo4j import Session

router = APIRouter()

def get_graph_service(neo4j_session: Session = Depends(get_neo4j)) -> Neo4jGraphService:
    return Neo4jGraphService(neo4j_session)

@router.get("")
def get_network(limit: int = Query(500, le=1000), graph_service: Neo4jGraphService = Depends(get_graph_service)):
    # Note: Returning the entire network is not recommended for large graphs.
    # We will limit the return to a bounded query.
    query = f"""
    MATCH (source)-[r]->(target)
    RETURN source.id AS source, target.id AS target, type(r) AS type,
           r.label AS label, r.confidence AS confidence, r.sourceRecord AS sourceRecord,
           r.timestamp AS timestamp
    LIMIT {limit}
    """
    result = graph_service.session.run(query)
    edges = []
    seen_nodes = set()
    for record in result:
        edges.append({
            "source": record["source"],
            "target": record["target"],
            "type": record["type"].lower(),
            "label": record.get("label", ""),
            "confidence": record.get("confidence", 100),
            "sourceRecord": record.get("sourceRecord", ""),
            "timestamp": record.get("timestamp")
        })
        seen_nodes.add(record["source"])
        seen_nodes.add(record["target"])
        
    return {
        "nodes": [{"id": node_id} for node_id in seen_nodes],
        "edges": edges
    }

@router.get("/entity/{entity_id}/network")
def get_entity_network(
    entity_id: str, 
    max_depth: int = Query(3, ge=1, le=5),
    graph_service: Neo4jGraphService = Depends(get_graph_service)
):
    if not entity_id:
        raise HTTPException(status_code=400, detail="entity_id is required")
        
    network = graph_service.get_multi_hop_network(entity_id, max_depth)
    if not network or not network["nodes"]:
        return {"nodes": [], "edges": []}
        
    # Map 'relationships' back to 'edges' for frontend compatibility if needed
    return {
        "nodes": network["nodes"],
        "edges": network["relationships"]
    }

@router.get("/shortest-path")
def get_shortest_path(
    source: str = Query(...), 
    target: str = Query(...), 
    max_depth: int = Query(4, ge=1, le=6),
    graph_service: Neo4jGraphService = Depends(get_graph_service)
):
    if not source or not target:
        raise HTTPException(status_code=400, detail="source and target are required")
        
    path_info = graph_service.find_shortest_path(source, target, max_depth)
    if not path_info:
        return {"path": [], "nodes": [], "edges": [], "message": "No path found"}
        
    return {
        "path": path_info["path"],
        "nodes": path_info["nodes"],
        "edges": path_info["relationships"],
        "path_length": path_info["path_length"]
    }

@router.get("/common-connections")
def get_common_connections(
    source: str = Query(...), 
    target: str = Query(...),
    graph_service: Neo4jGraphService = Depends(get_graph_service)
):
    if not source or not target:
        raise HTTPException(status_code=400, detail="source and target are required")
        
    common = graph_service.get_common_connections(source, target)
    return {"common_connections": common}

@router.get("/case/{case_id}/network")
def get_case_network(
    case_id: str,
    graph_service: Neo4jGraphService = Depends(get_graph_service)
):
    if not case_id:
        raise HTTPException(status_code=400, detail="case_id is required")
        
    network = graph_service.get_case_network(case_id)
    return {
        "nodes": network["nodes"],
        "edges": network["relationships"]
    }

@router.get("/metrics/{entity_id}")
def get_metrics(
    entity_id: str,
    graph_service: Neo4jGraphService = Depends(get_graph_service)
):
    if not entity_id:
        raise HTTPException(status_code=400, detail="entity_id is required")
        
    metrics = graph_service.get_graph_metrics(entity_id)
    return metrics
