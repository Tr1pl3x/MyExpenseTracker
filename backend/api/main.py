# backend/api/main.py
from __future__ import annotations

import os
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import JSONResponse

from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from .limits import limiter  # shared limiter instance

# Routers
from .routers import auth as auth_router
from .routers import categories as categories_router
from .routers import expenses as expenses_router
from .routers import stats as stats_router
from .routers import reports as reports_router

app = FastAPI(title="Expense Tracker API")

# ---- CORS ----
_default_origins = ["http://localhost:5173", "http://localhost:3000"]
origins_env = os.getenv("FRONTEND_ORIGINS", "")
origins = [o.strip() for o in origins_env.split(",") if o.strip()] or _default_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# ---- Compression ----
app.add_middleware(GZipMiddleware, minimum_size=500)

# ---- Trusted hosts (only if set)
hosts_env = os.getenv("ALLOWED_HOSTS", "").strip()
if hosts_env:
    hosts = [h.strip() for h in hosts_env.split(",") if h.strip()]
    if hosts:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=hosts)

# ---- HTTPS redirect (behind HTTPS)
if os.getenv("FORCE_HTTPS", "0") == "1":
    app.add_middleware(HTTPSRedirectMiddleware)

# ---- Security headers ----
@app.middleware("http")
async def security_headers(request: Request, call_next):
    resp = await call_next(request)
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "DENY")
    resp.headers.setdefault("Referrer-Policy", "no-referrer")
    if request.url.scheme == "https":
        resp.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=63072000; includeSubDomains; preload",
        )
    return resp

# ---- Rate limiting (global + per-route in routers)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    lambda r, e: JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"}),
)
app.add_middleware(SlowAPIMiddleware)

# ---- Routers ----
app.include_router(auth_router.router)
app.include_router(categories_router.router)
app.include_router(expenses_router.router)
app.include_router(stats_router.router)
app.include_router(reports_router.router)

# ---- Health ----
@app.get("/health")
def health():
    return {"ok": True}
