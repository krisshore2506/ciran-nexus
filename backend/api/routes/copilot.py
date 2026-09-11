from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from api.state import state
from models.domain import ChatMessage

router = APIRouter()

class CopilotRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    conversation_history: Optional[List[ChatMessage]] = Field(default=None, max_length=50)

@router.post("/query")
def ask_copilot(req: CopilotRequest):
    try:
        req.query = req.query.strip()
        if not req.query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
            
        return state.llm_service.generate_copilot_response(req.query, state, state.query_parser, req.conversation_history)
    except HTTPException:
        raise
    except Exception as e:
        # Log minimal error internally, do not leak stack trace
        import logging
        logging.error(f"Copilot processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal processing failure in Copilot service")

