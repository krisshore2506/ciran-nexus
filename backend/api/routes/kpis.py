from fastapi import APIRouter
from api.state import state

router = APIRouter()

@router.get("")
def get_kpis():
    active_cases = len([e for e in state.entities if e.type == "case"])
    high_priority_alerts = len([a for a in state.alerts if a.severity in ["critical", "high"]])
    total_entities = len(state.entities)
    cross_case_links = len(state.cross_case_links)
    
    return [
        {"label": "Active Investigations", "value": str(active_cases), "delta": "+2 this week", "tone": "info"},
        {"label": "High-Priority Signals", "value": str(high_priority_alerts), "delta": "Needs review", "tone": "critical"},
        {"label": "Total Entities", "value": str(total_entities), "delta": "Updated today", "tone": "high"},
        {"label": "Cross-Case Links", "value": str(cross_case_links), "delta": "New links found", "tone": "medium"},
    ]
