from datetime import date, datetime, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func

from ..db import engine
from ..models import Expense
from .auth import require_user

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/today")
def today_total(user_id: int = Depends(require_user)):
    # We store spent_at in UTC; use today's date in UTC to match.
    today_utc = datetime.now(timezone.utc).date()
    with Session(engine) as s:
        cents = s.exec(
            select(func.coalesce(func.sum(Expense.amount_cents), 0))
            .where(
                Expense.user_id == user_id,
                func.date(Expense.spent_at) == today_utc,
            )
        ).one()
        return {"day": today_utc.isoformat(), "total": cents / 100.0, "currency": "AUD"}

@router.get("/total")
def total_spent(
    user_id: int = Depends(require_user),
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
):
    with Session(engine) as s:
        stmt = (
            select(func.coalesce(func.sum(Expense.amount_cents), 0))
            .where(Expense.user_id == user_id)
        )
        if start:
            stmt = stmt.where(func.date(Expense.spent_at) >= start)
        if end:
            stmt = stmt.where(func.date(Expense.spent_at) <= end)
        cents = s.exec(stmt).one()
        return {"total": cents / 100.0, "currency": "AUD"}

@router.get("/by-category")
def by_category(
    user_id: int = Depends(require_user),
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
) -> List[dict]:
    with Session(engine) as s:
        cat = func.coalesce(Expense.category, "uncategorized")
        stmt = (
            select(
                cat.label("category"),
                func.sum(Expense.amount_cents).label("cents"),
                func.count().label("count"),
            )
            .where(Expense.user_id == user_id)
        )
        if start:
            stmt = stmt.where(func.date(Expense.spent_at) >= start)
        if end:
            stmt = stmt.where(func.date(Expense.spent_at) <= end)
        stmt = stmt.group_by(cat).order_by(func.sum(Expense.amount_cents).desc())
        rows = s.exec(stmt).all()
        return [
            {
                "category": r.category,
                "total": r.cents / 100.0,
                "count": r.count,
                "currency": "AUD",
            }
            for r in rows
        ]

@router.get("/daily")
def daily_totals(
    user_id: int = Depends(require_user),
    start: date = Query(..., description="Start date (inclusive)"),
    end:   date = Query(..., description="End date (inclusive)"),
) -> List[dict]:
    with Session(engine) as s:
        day_col = func.date(Expense.spent_at)
        stmt = (
            select(
                day_col.label("day"),
                func.sum(Expense.amount_cents).label("cents"),
            )
            .where(
                Expense.user_id == user_id,
                day_col >= start,
                day_col <= end,
            )
            .group_by(day_col)
            .order_by(day_col)
        )
        rows = s.exec(stmt).all()
        return [
            {"day": r.day.isoformat(), "total": r.cents / 100.0, "currency": "AUD"}
            for r in rows
        ]
