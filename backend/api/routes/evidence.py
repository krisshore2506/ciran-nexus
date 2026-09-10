from fastapi import APIRouter, HTTPException
from api.state import state

router = APIRouter()

@router.get("/{id}")
def get_evidence_item(id: str):
    for e in state.evidence:
        if e.id == id:
            return e
    raise HTTPException(status_code=404, detail="Evidence not found")
