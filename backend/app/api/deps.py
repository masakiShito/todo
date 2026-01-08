from typing import Generator
from ..db import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user_id() -> int:
    return 1
