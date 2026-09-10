from fastapi import APIRouter
from api.state import state

router = APIRouter()

@router.get("")
def get_cases():
    return [e for e in state.entities if e.type == "case"]
