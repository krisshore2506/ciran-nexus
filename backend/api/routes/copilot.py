from fastapi import APIRouter
from pydantic import BaseModel
from api.state import state

router = APIRouter()

class CopilotRequest(BaseModel):
    query: str

@router.post("/query")
def ask_copilot(req: CopilotRequest):
    return state.llm_service.generate_copilot_response(req.query, state, state.query_parser)
