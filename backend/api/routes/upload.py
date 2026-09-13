from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from config.db import get_db
from config.neo4j import get_neo4j
from services.ingestion_service import IngestionService

router = APIRouter()

@router.post("")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    neo4j_session = Depends(get_neo4j)
):
    """
    Ingest a raw document (TXT, PDF, JSON, CSV), extract entities and relationships, 
    and store them directly in PostgreSQL and Neo4j.
    """
    
    content = await file.read()
    
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        
    mime_type = file.content_type or "application/octet-stream"
    
    service = IngestionService(db, neo4j_session)
    result = service.process_document(file.filename, content, mime_type)
    
    if result["status"] == "failed":
        # Return 500 but still provide the record_id for traceability
        raise HTTPException(status_code=500, detail=result)
        
    return result
