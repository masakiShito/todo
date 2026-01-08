from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ... import crud, models, schemas
from ..deps import get_db, get_current_user_id

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return crud.get_categories(db, user_id)


@router.post("", response_model=schemas.CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(payload: schemas.CategoryCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return crud.create_category(db, user_id, payload)


@router.patch("/{category_id}", response_model=schemas.CategoryOut)
def update_category(category_id: int, payload: schemas.CategoryUpdate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    category = db.get(models.Category, category_id)
    if not category or category.user_id != user_id:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.update_category(db, category, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    category = db.get(models.Category, category_id)
    if not category or category.user_id != user_id:
        raise HTTPException(status_code=404, detail="Category not found")
    crud.delete_category(db, category)
    return None
