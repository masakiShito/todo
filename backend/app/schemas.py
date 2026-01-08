from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .models import TaskStatus, TaskPriority


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[dict] = None


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    color: Optional[str] = Field(None, max_length=30)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=30)


class CategoryOut(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.backlog
    priority: TaskPriority = TaskPriority.p2
    difficulty: int = Field(3, ge=1, le=5)
    category_id: Optional[int] = None
    due_date: Optional[date] = None
    start_date: Optional[date] = None
    estimate_hours: Optional[int] = Field(None, ge=1)
    tags: Optional[List[str]] = None
    parent_task_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    category_id: Optional[int] = None
    due_date: Optional[date] = None
    start_date: Optional[date] = None
    estimate_hours: Optional[int] = Field(None, ge=1)
    tags: Optional[List[str]] = None
    parent_task_id: Optional[int] = None
    order_index: Optional[int] = None
    is_deleted: Optional[bool] = None


class TaskMove(BaseModel):
    status: TaskStatus
    order_index: int = Field(..., ge=0)


class TaskOut(TaskBase):
    id: int
    order_index: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    items: List[TaskOut]
    total: int


class TimelineQuery(BaseModel):
    start: date
    end: date
    status: Optional[TaskStatus] = None
    category_id: Optional[int] = None
    priority: Optional[TaskPriority] = None
    difficulty: Optional[int] = None


class DashboardSummary(BaseModel):
    overdue: int
    today: int
    this_week: int
    no_due: int


class DashboardUrgent(BaseModel):
    items: List[TaskOut]
