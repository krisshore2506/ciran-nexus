import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from api.state import state
from models.domain import ChatMessage
from services.ciran_graph import CIRANGraphService
from config.db import get_db
from config.neo4j import get_neo4j
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger("copilot.audit")
logger.setLevel(logging.INFO)

class CopilotRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    conversation_history: Optional[List[ChatMessage]] = Field(default=None, max_length=50)

@router.post("/query")
def ask_copilot(
    req: CopilotRequest, 
    db: Session = Depends(get_db), 
    neo4j_session = Depends(get_neo4j)
):
    try:
        req.query = req.query.strip()
        if not req.query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
            
        graph_service = CIRANGraphService(db, neo4j_session)
        res = graph_service.invoke(req.query)
        
        logger.info(
            f"COPILOT_QUERY | Intent: {res.intent} | "
            f"Entities Referenced: {len(res.referenced_entities) if res.referenced_entities else 0} | "
            f"Sources: {res.source_count} | Success: True"
        )
        return res
    except HTTPException as e:
        logger.warning(f"COPILOT_QUERY | Status: {e.status_code} | Success: False")
        raise
    except Exception as e:
        logger.error(f"COPILOT_QUERY | Status: 500 | Success: False | Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal processing failure in Copilot service")

