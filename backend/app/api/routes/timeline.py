from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ... import crud, models, schemas
from ..deps import get_db, get_current_user_id

router = APIRouter(prefix="/api/timeline", tags=["timeline"])


@router.get("", response_model=list[schemas.TaskOut])
def get_timeline(
    start: date = Query(...),
    end: date = Query(...),
    status: models.TaskStatus | None = None,
    category_id: int | None = None,
    priority: models.TaskPriority | None = None,
    difficulty: int | None = Query(None, ge=1, le=5),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return crud.timeline_tasks(db, user_id, start, end, status, category_id, priority, difficulty)
