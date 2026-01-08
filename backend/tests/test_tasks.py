import os
from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.db import Base
from app.main import app
from app.api.deps import get_db

engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_update_list_task():
    category_resp = client.post("/api/categories", json={"name": "テスト", "color": "#CCE0F4"})
    assert category_resp.status_code == 201
    category_id = category_resp.json()["id"]

    create_resp = client.post(
        "/api/tasks",
        json={
            "title": "テストタスク",
            "description": "説明",
            "priority": "P1",
            "difficulty": 4,
            "category_id": category_id,
            "due_date": date.today().isoformat(),
            "status": "backlog",
        },
    )
    assert create_resp.status_code == 201
    task_id = create_resp.json()["id"]

    update_resp = client.patch(f"/api/tasks/{task_id}", json={"status": "in_progress", "order_index": 2})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "in_progress"

    list_resp = client.get("/api/tasks")
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert data["total"] >= 1
