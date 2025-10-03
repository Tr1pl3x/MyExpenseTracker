from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from ..db import engine
from ..models import Category
from .auth import require_user

router = APIRouter(prefix="/categories", tags=["categories"])

def _norm(name: str) -> str:
    return name.strip().lower()

class CategoryOut(BaseModel):
    id: int
    name: str
    is_default: bool

class CategoryCreate(BaseModel):
    name: str

@router.get("", response_model=List[CategoryOut])
def list_categories(user_id: int = Depends(require_user)):
    with Session(engine) as s:
        rows = s.exec(select(Category).where(Category.user_id == user_id).order_by(Category.name)).all()
        return [CategoryOut(id=r.id, name=r.name, is_default=r.is_default) for r in rows]

@router.post("", response_model=CategoryOut, status_code=201)
def create_category(data: CategoryCreate, user_id: int = Depends(require_user)):
    name = data.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Name required")
    norm = _norm(name)
    with Session(engine) as s:
        exists = s.exec(select(Category).where(Category.user_id == user_id, Category.normalized_name == norm)).first()
        if exists:
            raise HTTPException(status_code=409, detail="Category already exists")
        c = Category(user_id=user_id, name=name, normalized_name=norm, is_default=False)
        s.add(c); s.commit(); s.refresh(c)
        return CategoryOut(id=c.id, name=c.name, is_default=c.is_default)

@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, user_id: int = Depends(require_user)):
    with Session(engine) as s:
        c = s.get(Category, category_id)
        if not c or c.user_id != user_id:
            raise HTTPException(status_code=404, detail="Not found")
        if c.is_default:
            raise HTTPException(status_code=400, detail="Cannot delete default categories")
        s.delete(c); s.commit()
        return
