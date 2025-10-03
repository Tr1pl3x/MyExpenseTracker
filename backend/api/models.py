from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint, Column, DateTime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    display_name: Optional[str] = None


class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    amount_cents: int
    currency: str = "AUD"
    # NEW: store FK instead of free-text
    category_id: Optional[int] = Field(default=None, index=True, foreign_key="category.id")
    note: Optional[str] = None
    spent_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                 sa_column=Column(DateTime(timezone=True)))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                 sa_column=Column(DateTime(timezone=True)))

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    name: str                              # display value (original casing)
    normalized_name: str = Field(index=True)  # e.g., "food"
    is_default: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True))
    )

    __table_args__ = (
        UniqueConstraint("user_id", "normalized_name", name="uq_category_user_norm"),
    )