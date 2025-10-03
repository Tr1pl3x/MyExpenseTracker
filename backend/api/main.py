from fastapi import FastAPI
from .db import init_db
from .routers import auth as auth_router
from .routers import expenses as expenses_router
from .routers import stats as stats_router

app = FastAPI(title="Expense Tracker API")

app.include_router(auth_router.router)
app.include_router(expenses_router.router)
app.include_router(stats_router.router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True}
