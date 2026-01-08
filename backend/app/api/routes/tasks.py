from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ... import crud, models, schemas
from ..deps import get_db, get_current_user_id

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=schemas.TaskList)
def list_tasks(
    status: models.TaskStatus | None = None,
    category_id: int | None = None,
    priority: models.TaskPriority | None = None,
    due_from: date | None = None,
    due_to: date | None = None,
    parent_task_id: int | None = None,
    search: str | None = None,
    sort: str = Query("due_date", pattern="^(due_date|created_at|priority)$"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    items, total = crud.list_tasks(
        db,
        user_id,
        status=status,
        category_id=category_id,
        priority=priority,
        due_from=due_from,
        due_to=due_to,
        parent_task_id=parent_task_id,
        search=search,
        sort=sort,
        page=page,
        per_page=per_page,
    )
    return schemas.TaskList(items=items, total=total)


@router.post("", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return crud.create_task(db, user_id, payload)


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    task = crud.get_task(db, user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    task = crud.get_task(db, user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db, task, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    task = crud.get_task(db, user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.soft_delete_task(db, task)
    return None


@router.post("/{task_id}/move", response_model=schemas.TaskOut)
def move_task(task_id: int, payload: schemas.TaskMove, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    task = crud.get_task(db, user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.move_task(db, task, payload.status, payload.order_index)
