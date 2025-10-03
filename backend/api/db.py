# backend/api/db.py
from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

# --- Load .env for local dev (search backend/.env then repo/.env) ---
try:
    from dotenv import load_dotenv  # type: ignore
except Exception:  # python-dotenv not installed in prod serverless
    load_dotenv = None  # graceful fallback

if load_dotenv:
    # current file: backend/api/db.py
    candidates = [
        Path(__file__).resolve().parents[1] / ".env",  # backend/.env
        Path(__file__).resolve().parents[2] / ".env",  # repo/.env (if you ever move root)
    ]
    for p in candidates:
        if p.exists():
            load_dotenv(p)  # load first found .env
            break
    else:
        # fall back to default search locations (optional)
        load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Create backend/.env with DATABASE_URL=... "
        "or export it in your shell."
    )

# Use NullPool in serverless (Vercel) to avoid long-lived pools.
IS_SERVERLESS = os.getenv("VERCEL") == "1" or os.getenv("SERVERLESS") == "1"

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool if IS_SERVERLESS else None,  # None -> default pool locally
    pool_pre_ping=True,
)
