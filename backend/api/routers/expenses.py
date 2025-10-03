# api/routers/expenses.py
from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone
from typing import List, Optional
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field as PydField
from sqlmodel import Session, select

from ..db import engine
from ..models import Expense, Category
from .auth import require_user
from ..limits import limiter

router = APIRouter(prefix="/expenses", tags=["expenses"])

# ---------- Schemas ----------

class ExpenseIn(BaseModel):
    amount: float = PydField(gt=0, description="Amount in dollars")
    currency: str = "AUD"
    category_id: int  # required & validated
    note: Optional[str] = None
    spent_at: Optional[datetime] = None  # ISO 8601; if omitted -> now (UTC)

class ExpenseOut(BaseModel):
    id: int
    amount: float
    currency: str
    category_id: Optional[int]
    note: Optional[str]
    spent_at: datetime

# ---------- Helpers ----------

def _tz() -> ZoneInfo:
    return ZoneInfo(os.getenv("APP_TZ", "UTC"))

def _day_bounds_utc(d: date, tz: ZoneInfo) -> tuple[datetime, datetime]:
    """Given a local date (in tz), return [start,end) in UTC."""
    start_local = datetime(d.year, d.month, d.day, tzinfo=tz)
    end_local = start_local + timedelta(days=1)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)

def _to_out(e: Expense) -> ExpenseOut:
    return ExpenseOut(
        id=e.id,
        amount=e.amount_cents / 100.0,
        currency=e.currency,
        category_id=e.category_id,
        note=e.note,
        spent_at=e.spent_at,
    )

def _validate_category_belongs(s: Session, user_id: int, category_id: int) -> None:
    c = s.get(Category, category_id)
    if not c or c.user_id != user_id:
        raise HTTPException(status_code=400, detail="Invalid category_id")

# ---------- Routes ----------

@router.post("", response_model=ExpenseOut, status_code=201)
@limiter.limit(os.getenv("RATE_LIMIT_WRITES", "60/minute"))
def create_expense(
    data: ExpenseIn,
    request: Request,
    user_id: int = Depends(require_user),
):
    """Create an expense; stores UTC timestamps; validates category_id ownership."""
    with Session(engine) as s:
        _validate_category_belongs(s, user_id, data.category_id)

        ts = data.spent_at.astimezone(timezone.utc) if data.spent_at else datetime.now(timezone.utc)

        e = Expense(
            user_id=user_id,
            amount_cents=int(round(data.amount * 100)),
            currency=data.currency,
            category_id=data.category_id,
            note=data.note,
            spent_at=ts,
        )
        s.add(e)
        s.commit()
        s.refresh(e)
        return _to_out(e)

@router.get("", response_model=List[ExpenseOut])
def list_expenses(
    user_id: int = Depends(require_user),
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List expenses (newest first). Optional date range in APP_TZ local dates."""
    tz = _tz()
    with Session(engine) as s:
        stmt = select(Expense).where(Expense.user_id == user_id)

        if start:
            start_utc, _ = _day_bounds_utc(start, tz)
            stmt = stmt.where(Expense.spent_at >= start_utc)
        if end:
            _, end_utc = _day_bounds_utc(end, tz)
            stmt = stmt.where(Expense.spent_at < end_utc)

        stmt = stmt.order_by(Expense.spent_at.desc(), Expense.id.desc()).limit(limit).offset(offset)
        rows = s.exec(stmt).all()
        return [_to_out(r) for r in rows]

# Place this BEFORE the /{expense_id} routes and constrain those to :int
@router.get("/today", response_model=List[ExpenseOut])
def list_today(user_id: int = Depends(require_user)):
    """List today's expenses in APP_TZ (default UTC), newest first."""
    tz = _tz()
    today_local = datetime.now(tz).date()
    start_utc, end_utc = _day_bounds_utc(today_local, tz)

    with Session(engine) as s:
        stmt = (
            select(Expense)
            .where(
                Expense.user_id == user_id,
                Expense.spent_at >= start_utc,
                Expense.spent_at < end_utc,
            )
            .order_by(Expense.spent_at.desc(), Expense.id.desc())
        )
        rows = s.exec(stmt).all()
        return [_to_out(r) for r in rows]

@router.get("/{expense_id:int}", response_model=ExpenseOut)
def get_expense(expense_id: int, user_id: int = Depends(require_user)):
    with Session(engine) as s:
        e = s.get(Expense, expense_id)
        if not e or e.user_id != user_id:
            raise HTTPException(status_code=404, detail="Not found")
        return _to_out(e)

@router.put("/{expense_id:int}", response_model=ExpenseOut)
@limiter.limit(os.getenv("RATE_LIMIT_WRITES", "60/minute"))
def update_expense(
    expense_id: int,
    data: ExpenseIn,
    request: Request,
    user_id: int = Depends(require_user),
):
    with Session(engine) as s:
        e = s.get(Expense, expense_id)
        if not e or e.user_id != user_id:
            raise HTTPException(status_code=404, detail="Not found")

        _validate_category_belongs(s, user_id, data.category_id)

        e.amount_cents = int(round(data.amount * 100))
        e.currency = data.currency
        e.category_id = data.category_id
        e.note = data.note
        if data.spent_at:
            e.spent_at = data.spent_at.astimezone(timezone.utc)
        e.updated_at = datetime.now(timezone.utc)

        s.add(e)
        s.commit()
        s.refresh(e)
        return _to_out(e)

@router.delete("/{expense_id:int}", status_code=204)
@limiter.limit(os.getenv("RATE_LIMIT_WRITES", "60/minute"))
def delete_expense(expense_id: int, request: Request, user_id: int = Depends(require_user)):
    with Session(engine) as s:
        e = s.get(Expense, expense_id)
        if not e or e.user_id != user_id:
            raise HTTPException(status_code=404, detail="Not found")
        s.delete(e)
        s.commit()
        return

@router.get("/by-category/{category_id:int}", response_model=List[ExpenseOut])
def list_by_category(
    category_id: int,
    user_id: int = Depends(require_user),
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List expenses for a category, newest first. Validates category ownership."""
    tz = _tz()
    with Session(engine) as s:
        _validate_category_belongs(s, user_id, category_id)

        stmt = select(Expense).where(
            Expense.user_id == user_id,
            Expense.category_id == category_id,
        )

        if start:
            start_utc, _ = _day_bounds_utc(start, tz)
            stmt = stmt.where(Expense.spent_at >= start_utc)
        if end:
            _, end_utc = _day_bounds_utc(end, tz)
            stmt = stmt.where(Expense.spent_at < end_utc)

        stmt = stmt.order_by(Expense.spent_at.desc(), Expense.id.desc()).limit(limit).offset(offset)
        rows = s.exec(stmt).all()
        return [_to_out(r) for r in rows]
