from fastapi import APIRouter
from api.state import state

router = APIRouter()

@router.get("")
def get_alerts():
    return state.alerts
