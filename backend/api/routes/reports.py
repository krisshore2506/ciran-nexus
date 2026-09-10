from fastapi import APIRouter
from api.state import state

router = APIRouter()

@router.post("/generate")
def generate_report():
    return state.report_generator.generate_report(state.entities, state.cross_case_links, state.alerts)
