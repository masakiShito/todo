from datetime import date, timedelta
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Category, Task, TaskStatus, TaskPriority


def run_seed():
    db: Session = SessionLocal()
    try:
        if db.query(Category).count() > 0:
            return
        work = Category(user_id=1, name="仕事", color="#BFD7EA")
        personal = Category(user_id=1, name="個人", color="#CDEAC0")
        db.add_all([work, personal])
        db.flush()
        tasks = [
            Task(
                user_id=1,
                title="Backlog風TODOの設計",
                description="親タスク: 全体設計",
                status=TaskStatus.backlog,
                priority=TaskPriority.p1,
                difficulty=3,
                category_id=work.id,
                due_date=date.today() + timedelta(days=5),
                start_date=date.today(),
                estimate_hours=6,
                tags=["design", "planning"],
                order_index=0,
            ),
            Task(
                user_id=1,
                title="ダッシュボードUI",
                description="ウィジェット整理",
                status=TaskStatus.in_progress,
                priority=TaskPriority.p0,
                difficulty=4,
                category_id=work.id,
                due_date=date.today() + timedelta(days=2),
                start_date=date.today(),
                estimate_hours=8,
                tags=["ui"],
                order_index=1,
            ),
            Task(
                user_id=1,
                title="買い物リスト整理",
                description="冷蔵庫の補充",
                status=TaskStatus.review,
                priority=TaskPriority.p2,
                difficulty=2,
                category_id=personal.id,
                due_date=date.today() + timedelta(days=1),
                start_date=date.today(),
                estimate_hours=1,
                tags=["home"],
                order_index=0,
            ),
            Task(
                user_id=1,
                title="本の読了",
                description="子タスクを含む",
                status=TaskStatus.backlog,
                priority=TaskPriority.p3,
                difficulty=2,
                category_id=personal.id,
                due_date=None,
                start_date=date.today() + timedelta(days=3),
                estimate_hours=5,
                tags=["study"],
                order_index=2,
            ),
        ]
        db.add_all(tasks)
        db.flush()
        child = Task(
            user_id=1,
            title="第1章を読む",
            description="子タスク",
            status=TaskStatus.backlog,
            priority=TaskPriority.p2,
            difficulty=1,
            category_id=personal.id,
            parent_task_id=tasks[-1].id,
            due_date=date.today() + timedelta(days=4),
            order_index=0,
        )
        db.add(child)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
