import os
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from datetime import datetime, timezone  # ad
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field as PydField
from sqlmodel import Session, select
from ..db import engine
from ..models import Expense
from .auth import require_user
import os


router = APIRouter(prefix="/expenses", tags=["expenses"])

class ExpenseIn(BaseModel):
    amount: float = PydField(gt=0)          # dollars
    currency: str = "AUD"
    category: Optional[str] = None
    note: Optional[str] = None
    spent_at: Optional[datetime] = None  # <-- allow time; optional

class ExpenseOut(BaseModel):
    id: int
    amount: float
    currency: str
    category: Optional[str]
    note: Optional[str]
    spent_at: datetime  # Pydantic will emit ISO 8601 with time

def to_out(e: Expense) -> ExpenseOut:
    return ExpenseOut(
        id=e.id, amount=e.amount_cents / 100.0, currency=e.currency,
        category=e.category, note=e.note, spent_at=e.spent_at
    )

@router.post("", response_model=ExpenseOut, status_code=201)
def create_expense(data: ExpenseIn, user_id: int = Depends(require_user)):
    ts = data.spent_at.astimezone(timezone.utc) if data.spent_at else datetime.now(timezone.utc)
    with Session(engine) as s:
        e = Expense(
            user_id=user_id,
            amount_cents=int(round(data.amount * 100)),
            currency=data.currency,
            category=data.category,
            note=data.note,
            spent_at=ts,
        )
        s.add(e); s.commit(); s.refresh(e)
        return to_out(e)

@router.get("/today", response_model=List[ExpenseOut])
def list_today(user_id: int = Depends(require_user)):
    tz = ZoneInfo(os.getenv("APP_TZ", "UTC"))
    now_local = datetime.now(tz)
    start_local = datetime(now_local.year, now_local.month, now_local.day, tzinfo=tz)
    end_local = start_local + timedelta(days=1)

    # Convert to UTC because we store spent_at as UTC
    start_utc = start_local.astimezone(timezone.utc)
    end_utc = end_local.astimezone(timezone.utc)

    with Session(engine) as s:
        stmt = (
            select(Expense)
            .where(
                Expense.user_id == user_id,
                Expense.spent_at >= start_utc,
                Expense.spent_at < end_utc,
            )
            .order_by(Expense.spent_at.desc())
        )
        rows = s.exec(stmt).all()
        return [to_out(r) for r in rows]

@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int, user_id: int = Depends(require_user)):
    with Session(engine) as s:
        e = s.get(Expense, expense_id)
        if not e or e.user_id != user_id:
            raise HTTPException(status_code=404, detail="Not found")
        return to_out(e)

@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, data: ExpenseIn, user_id: int = Depends(require_user)):
    with Session(engine) as s:
        e = s.get(Expense, expense_id)
        if not e or e.user_id != user_id:
            raise HTTPException(status_code=404, detail="Not found")
        e.amount_cents = int(round(data.amount * 100))
        e.currency = data.currency
        e.category = data.category
        e.note = data.note
        e.spent_at = data.spent_at
        e.updated_at = datetime.utcnow()
        s.add(e); s.commit(); s.refresh(e)
        return to_out(e)

@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: int, user_id: int = Depends(require_user)):
    with Session(engine) as s:
        e = s.get(Expense, expense_id)
        if not e or e.user_id != user_id:
            raise HTTPException(status_code=404, detail="Not found")
        s.delete(e); s.commit()
        return
