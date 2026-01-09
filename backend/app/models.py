import enum
from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    Index,
    JSON,
)
from sqlalchemy.orm import relationship
from .db import Base


class TaskStatus(str, enum.Enum):
    backlog = "backlog"
    in_progress = "in_progress"
    review = "review"
    done = "done"


class TaskPriority(str, enum.Enum):
    p0 = "P0"
    p1 = "P1"
    p2 = "P2"
    p3 = "P3"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True, default=1)
    name = Column(String(100), nullable=False)
    color = Column(String(30), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tasks = relationship("Task", back_populates="category")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True, default=1)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.backlog)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.p2)
    difficulty = Column(Integer, nullable=False, default=3)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    due_date = Column(Date, nullable=True)
    start_date = Column(Date, nullable=True)
    estimate_hours = Column(Integer, nullable=True)
    tags = Column(JSON, nullable=True)
    parent_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    order_index = Column(Integer, nullable=False, default=0)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    category = relationship("Category", back_populates="tasks")
    parent = relationship("Task", remote_side=[id], backref="children")


Index("idx_tasks_status", Task.status)
Index("idx_tasks_due_date", Task.due_date)
Index("idx_tasks_category", Task.category_id)
Index("idx_tasks_parent", Task.parent_task_id)
