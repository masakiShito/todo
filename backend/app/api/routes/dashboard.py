from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ... import crud, schemas
from ..deps import get_db, get_current_user_id

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=schemas.DashboardSummary)
def summary(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return crud.dashboard_summary(db, user_id)


@router.get("/urgent", response_model=schemas.DashboardUrgent)
def urgent(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    items = crud.dashboard_urgent(db, user_id)
    return schemas.DashboardUrgent(items=items)
