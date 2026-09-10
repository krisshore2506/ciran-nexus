from fastapi import APIRouter
from api.state import state

router = APIRouter()

@router.get("")
def get_network():
    return {
        "nodes": state.entities,
        "edges": state.relations
    }
