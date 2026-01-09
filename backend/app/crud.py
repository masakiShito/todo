from datetime import date, timedelta
from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from . import models


def get_categories(db: Session, user_id: int):
    return db.scalars(select(models.Category).where(models.Category.user_id == user_id)).all()


def create_category(db: Session, user_id: int, data):
    category = models.Category(user_id=user_id, **data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category: models.Category, data):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category: models.Category):
    db.delete(category)
    db.commit()


def get_task(db: Session, user_id: int, task_id: int):
    return db.scalar(select(models.Task).where(models.Task.user_id == user_id, models.Task.id == task_id, models.Task.is_deleted.is_(False)))


def list_tasks(
    db: Session,
    user_id: int,
    status: Optional[models.TaskStatus] = None,
    category_id: Optional[int] = None,
    priority: Optional[models.TaskPriority] = None,
    due_from: Optional[date] = None,
    due_to: Optional[date] = None,
    parent_task_id: Optional[int] = None,
    search: Optional[str] = None,
    sort: str = "due_date",
    page: int = 1,
    per_page: int = 20,
):
    query = select(models.Task).where(models.Task.user_id == user_id, models.Task.is_deleted.is_(False))
    if status:
        query = query.where(models.Task.status == status)
    if category_id:
        query = query.where(models.Task.category_id == category_id)
    if priority:
        query = query.where(models.Task.priority == priority)
    if due_from:
        query = query.where(models.Task.due_date >= due_from)
    if due_to:
        query = query.where(models.Task.due_date <= due_to)
    if parent_task_id is not None:
        query = query.where(models.Task.parent_task_id == parent_task_id)
    if search:
        query = query.where(models.Task.title.ilike(f"%{search}%"))

    if sort == "created_at":
        query = query.order_by(models.Task.created_at.desc())
    elif sort == "priority":
        query = query.order_by(models.Task.priority.asc())
    else:
        query = query.order_by(models.Task.due_date.asc().nulls_last())

    total = db.scalar(select(func.count()).select_from(query.subquery()))
    items = db.scalars(query.offset((page - 1) * per_page).limit(per_page)).all()
    return items, total


def create_task(db: Session, user_id: int, data):
    task = models.Task(user_id=user_id, **data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: models.Task, data):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def soft_delete_task(db: Session, task: models.Task):
    task.is_deleted = True
    db.commit()


def move_task(db: Session, task: models.Task, status: models.TaskStatus, order_index: int):
    task.status = status
    task.order_index = order_index
    db.commit()
    db.refresh(task)
    return task


def timeline_tasks(db: Session, user_id: int, start: date, end: date, status=None, category_id=None, priority=None, difficulty=None):
    query = select(models.Task).where(
        models.Task.user_id == user_id,
        models.Task.is_deleted.is_(False),
        models.Task.due_date.is_not(None),
        models.Task.due_date.between(start, end),
    )
    if status:
        query = query.where(models.Task.status == status)
    if category_id:
        query = query.where(models.Task.category_id == category_id)
    if priority:
        query = query.where(models.Task.priority == priority)
    if difficulty:
        query = query.where(models.Task.difficulty == difficulty)
    return db.scalars(query.order_by(models.Task.due_date.asc())).all()


def dashboard_summary(db: Session, user_id: int):
    today = date.today()
    end_week = today + timedelta(days=6)
    overdue = db.scalar(select(func.count()).select_from(models.Task).where(
        models.Task.user_id == user_id,
        models.Task.is_deleted.is_(False),
        models.Task.due_date < today,
        models.Task.status != models.TaskStatus.done,
    ))
    today_count = db.scalar(select(func.count()).select_from(models.Task).where(
        models.Task.user_id == user_id,
        models.Task.is_deleted.is_(False),
        models.Task.due_date == today,
        models.Task.status != models.TaskStatus.done,
    ))
    week_count = db.scalar(select(func.count()).select_from(models.Task).where(
        models.Task.user_id == user_id,
        models.Task.is_deleted.is_(False),
        models.Task.due_date >= today,
        models.Task.due_date <= end_week,
        models.Task.status != models.TaskStatus.done,
    ))
    no_due = db.scalar(select(func.count()).select_from(models.Task).where(
        models.Task.user_id == user_id,
        models.Task.is_deleted.is_(False),
        models.Task.due_date.is_(None),
        models.Task.status != models.TaskStatus.done,
    ))
    return dict(overdue=overdue, today=today_count, this_week=week_count, no_due=no_due)


def dashboard_urgent(db: Session, user_id: int, days: int = 7):
    today = date.today()
    end_date = today + timedelta(days=days)
    query = select(models.Task).where(
        models.Task.user_id == user_id,
        models.Task.is_deleted.is_(False),
        models.Task.status != models.TaskStatus.done,
        models.Task.due_date.is_not(None),
        models.Task.due_date.between(today, end_date),
    ).order_by(models.Task.due_date.asc())
    return db.scalars(query).all()
