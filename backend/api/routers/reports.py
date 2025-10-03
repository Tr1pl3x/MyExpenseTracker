# api/routers/reports.py
from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone
from typing import Optional, List
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlmodel import Session, select

from ..db import engine
from ..models import Expense, Category
from .auth import require_user

router = APIRouter(prefix="/reports", tags=["reports"])

# ---- helpers ---------------------------------------------------------------

def _tz() -> ZoneInfo:
    return ZoneInfo(os.getenv("APP_TZ", "UTC"))

def _day_bounds_utc(d: date, tz: ZoneInfo) -> tuple[datetime, datetime]:
    start_local = datetime(d.year, d.month, d.day, tzinfo=tz)
    end_local = start_local + timedelta(days=1)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)

def _default_period_local(now_local: datetime) -> tuple[date, date]:
    """First day of current month .. today (both local)."""
    start = date(now_local.year, now_local.month, 1)
    end = now_local.date()
    return start, end

def _iso_day(value) -> str:
    """Normalize DB 'date' values that may come back as date/datetime/str."""
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, datetime):
        return value.date().isoformat()
    return str(value)

# ---- /reports/summary ------------------------------------------------------

@router.get("/summary")
def summary(
    user_id: int = Depends(require_user),
    start: Optional[date] = Query(None, description="YYYY-MM-DD (local to APP_TZ)"),
    end: Optional[date] = Query(None, description="YYYY-MM-DD (local to APP_TZ)"),
    top_k: int = Query(6, ge=1, le=50, description="Max categories before bucketing 'Other'"),
):
    """
    One-call dashboard data:
      - period total
      - totals grouped by category (top_k + 'Other')
      - daily totals (UTC calendar days; filters respect APP_TZ)
    """
    tz = _tz()
    now_local = datetime.now(tz)
    if not start or not end:
        def_start, def_end = _default_period_local(now_local)
        start = start or def_start
        end = end or def_end

    # Convert local date bounds -> UTC [start, end)
    start_utc, _ = _day_bounds_utc(start, tz)
    _, end_utc = _day_bounds_utc(end, tz)

    with Session(engine) as s:
        # ---- total
        total_cents = s.exec(
            select(func.coalesce(func.sum(Expense.amount_cents), 0))
            .where(
                Expense.user_id == user_id,
                Expense.spent_at >= start_utc,
                Expense.spent_at < end_utc,
            )
        ).one()

        # ---- by category (LEFT JOIN so uncategorized shows up)
        cat_rows = s.exec(
            select(
                Expense.category_id,
                func.coalesce(Category.name, "uncategorized").label("name"),
                func.sum(Expense.amount_cents).label("cents"),
                func.count().label("count"),
            )
            .where(
                Expense.user_id == user_id,
                Expense.spent_at >= start_utc,
                Expense.spent_at < end_utc,
            )
            .join(
                Category,
                (Category.id == Expense.category_id) & (Category.user_id == user_id),
                isouter=True,
            )
            .group_by(Expense.category_id, Category.name)
            .order_by(func.sum(Expense.amount_cents).desc())
        ).all()

        by_category = [
            {"category_id": r.category_id, "name": r.name, "total": r.cents / 100.0, "count": r.count}
            for r in cat_rows
        ]

        # bucket "Other" if too many
        if len(by_category) > top_k:
            head = by_category[:top_k]
            tail = by_category[top_k:]
            other_total = sum(x["total"] for x in tail)
            other_count = sum(x["count"] for x in tail)
            head.append({"category_id": None, "name": "Other", "total": other_total, "count": other_count})
            by_category = head

        # ---- daily series
        day_col = func.date(Expense.spent_at)
        daily_rows = s.exec(
            select(day_col.label("day"), func.sum(Expense.amount_cents).label("cents"))
            .where(
                Expense.user_id == user_id,
                Expense.spent_at >= start_utc,
                Expense.spent_at < end_utc,
            )
            .group_by(day_col)
            .order_by(day_col)
        ).all()

        daily = [{"day": _iso_day(r.day), "total": r.cents / 100.0} for r in daily_rows]

    return {
        "period": {"start": start.isoformat(), "end": end.isoformat()},
        "currency": "AUD",
        "total": total_cents / 100.0,
        "by_category": by_category,
        "daily": daily,
    }
