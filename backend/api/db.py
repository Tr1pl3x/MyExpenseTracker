# api/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

DATABASE_URL = os.getenv("DATABASE_URL")

# Vercel sets VERCEL=1. Also allow opt-in via SERVERLESS=1.
IS_SERVERLESS = os.getenv("VERCEL") == "1" or os.getenv("SERVERLESS") == "1"

# For serverless: use NullPool (no long-lived pools)
if IS_SERVERLESS:
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
        pool_pre_ping=True,
    )
else:
    # your previous engine (e.g., default pool)
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
    )