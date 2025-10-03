# api/routers/stats.py
from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone
from typing import List, Optional
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from sqlalchemy import func

from ..db import engine
from ..models import Expense, Category
from .auth import require_user

router = APIRouter(prefix="/stats", tags=["stats"])

# ---------- helpers ----------

def _tz() -> ZoneInfo:
    return ZoneInfo(os.getenv("APP_TZ", "UTC"))

def _day_bounds_utc(d: date, tz: ZoneInfo) -> tuple[datetime, datetime]:
    start_local = datetime(d.year, d.month, d.day, tzinfo=tz)
    end_local = start_local + timedelta(days=1)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)

def _iso_day(value) -> str:
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, datetime):
        return value.date().isoformat()
    return str(value)

# ---------- endpoints ----------

@router.get("/today")
def today_total(user_id: int = Depends(require_user)):
    tz = _tz()
    start_utc, end_utc = _day_bounds_utc(datetime.now(tz).date(), tz)
    with Session(engine) as s:
        cents = s.exec(
            select(func.coalesce(func.sum(Expense.amount_cents), 0))
            .where(
                Expense.user_id == user_id,
                Expense.spent_at >= start_utc,
                Expense.spent_at < end_utc,
            )
        ).one()
        return {"day": start_utc.date().isoformat(), "total": cents / 100.0, "currency": "AUD"}

@router.get("/total")
def total_spent(
    user_id: int = Depends(require_user),
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
):
    tz = _tz()
    with Session(engine) as s:
        stmt = select(func.coalesce(func.sum(Expense.amount_cents), 0)).where(Expense.user_id == user_id)
        if start:
            start_utc, _ = _day_bounds_utc(start, tz)
            stmt = stmt.where(Expense.spent_at >= start_utc)
        if end:
            _, end_utc = _day_bounds_utc(end, tz)
            stmt = stmt.where(Expense.spent_at < end_utc)
        cents = s.exec(stmt).one()
        return {"total": cents / 100.0, "currency": "AUD"}

@router.get("/total-by-category")
def total_by_category(
    user_id: int = Depends(require_user),
    start: Optional[date] = Query(None, description="YYYY-MM-DD"),
    end: Optional[date] = Query(None, description="YYYY-MM-DD"),
) -> List[dict]:
    """
    Returns totals grouped by category_id.
    [{ category_id, name, total, count, currency }]
    """
    tz = _tz()
    with Session(engine) as s:
        stmt = (
            select(
                Expense.category_id,
                func.coalesce(Category.name, "uncategorized").label("name"),
                func.sum(Expense.amount_cents).label("cents"),
                func.count().label("count"),
            )
            .where(Expense.user_id == user_id)
            .join(
                Category,
                (Category.id == Expense.category_id) & (Category.user_id == user_id),
                isouter=True,
            )
        )
        if start:
            start_utc, _ = _day_bounds_utc(start, tz)
            stmt = stmt.where(Expense.spent_at >= start_utc)
        if end:
            _, end_utc = _day_bounds_utc(end, tz)
            stmt = stmt.where(Expense.spent_at < end_utc)

        stmt = stmt.group_by(Expense.category_id, Category.name)\
                   .order_by(func.sum(Expense.amount_cents).asc())
        rows = s.exec(stmt).all()
        return [
            {
                "category_id": r.category_id,
                "name": r.name,
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
    """
    Groups by UTC calendar day. (Filters respect APP_TZ bounds.)
    """
    tz = _tz()
    start_utc, _ = _day_bounds_utc(start, tz)
    _, end_utc = _day_bounds_utc(end, tz)

    with Session(engine) as s:
        day_col = func.date(Expense.spent_at)
        stmt = (
            select(day_col.label("day"), func.sum(Expense.amount_cents).label("cents"))
            .where(
                Expense.user_id == user_id,
                Expense.spent_at >= start_utc,
                Expense.spent_at < end_utc,
            )
            .group_by(day_col)
            .order_by(day_col)
        )
        rows = s.exec(stmt).all()
        return [{"day": _iso_day(r.day), "total": r.cents / 100.0, "currency": "AUD"} for r in rows]
