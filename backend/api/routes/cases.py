from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db import get_db
from models.sql_models import Entity as SQLEntity
from models.domain import Entity

router = APIRouter()

@router.get("", response_model=list[Entity])
def get_cases(db: Session = Depends(get_db)):
    cases_db = db.query(SQLEntity).filter(SQLEntity.type == "case").all()
    # Map back to Pydantic if needed, but FastAPI does this automatically
    # as long as attributes match the schema.
    return cases_db
