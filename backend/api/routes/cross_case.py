from fastapi import APIRouter
from api.state import state

router = APIRouter()

@router.get("")
def get_cross_case():
    return state.cross_case_links
