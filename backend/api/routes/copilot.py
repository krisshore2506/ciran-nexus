import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from api.state import state
from models.domain import ChatMessage
from services.copilot_retrieval import CopilotRetrievalService
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
            
        retrieval_service = CopilotRetrievalService(db, neo4j_session)
        # Parse query intent
        structured_query = state.query_parser.parse_query(req.query, state.entities, req.conversation_history)
        extracted_entities = [e for e in state.entities if e.id in structured_query.entities]
        
        # Execute Vector + Graph Retrieval
        retrieval_result = retrieval_service.retrieve(structured_query, extracted_entities)
        
        # Pass to LLM Service for final formatting
        res = state.llm_service.generate_copilot_response_with_result(
            req.query, structured_query, extracted_entities, retrieval_result
        )
        
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

