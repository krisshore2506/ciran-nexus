import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from api.state import state
from models.domain import ChatMessage

router = APIRouter()
logger = logging.getLogger("copilot.audit")
logger.setLevel(logging.INFO)

class CopilotRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    conversation_history: Optional[List[ChatMessage]] = Field(default=None, max_length=50)

@router.post("/query")
def ask_copilot(req: CopilotRequest):
    try:
        req.query = req.query.strip()
        if not req.query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
            
        res = state.llm_service.generate_copilot_response(req.query, state, state.query_parser, req.conversation_history)
        
        # Safe Audit Logging (No PII, No raw query, No secrets)
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
        # Log minimal error internally, do not leak stack trace
        logger.error(f"COPILOT_QUERY | Status: 500 | Success: False | Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal processing failure in Copilot service")

