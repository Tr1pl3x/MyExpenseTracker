from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from ..db import engine
from ..models import User
from fastapi import Request
from ..limits import limiter
import os

from ..auth import hash_pw, verify_pw, make_token, decode_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

def _norm(name: str) -> str:
    return name.strip().lower()


router = APIRouter(prefix="/auth", tags=["auth"])
bearer = HTTPBearer()

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    display_name: str | None = None

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=TokenOut)
@limiter.limit(os.getenv("RATE_LIMIT_AUTH", "5/minute"))
def register(data: RegisterIn, request: Request):
    from ..models import User, Category
    from sqlmodel import Session, select

    def _norm(name: str) -> str:
        return name.strip().lower()

    defaults = ["bills", "food", "entertainment", "transportation", "shopping", "subscriptions"]

    with Session(engine) as s:
        # 1) Block duplicates
        if s.exec(select(User).where(User.email == data.email)).first():
            raise HTTPException(status_code=409, detail="Email already registered")

        # 2) Create user first and get its id
        u = User(email=data.email, password_hash=hash_pw(data.password), display_name=data.display_name)
        s.add(u); s.commit(); s.refresh(u)

        # 3) Seed default categories for this user
        for name in defaults:
            s.add(Category(
                user_id=u.id,
                name=name.capitalize(),
                normalized_name=_norm(name),
                is_default=True
            ))
        s.commit()

        # 4) Return token
        return TokenOut(access_token=make_token(str(u.id)))


class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/login", response_model=TokenOut)
@limiter.limit(os.getenv("RATE_LIMIT_AUTH", "5/minute"))
def login(data: LoginIn, request: Request):
    with Session(engine) as s:
        u = s.exec(select(User).where(User.email == data.email)).first()
        if not u or not verify_pw(data.password, u.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return TokenOut(access_token=make_token(str(u.id)))

def require_user(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> int:
    sub = decode_token(creds.credentials)
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(sub)

@router.get("/me")
def me(user_id: int = Depends(require_user)):
    with Session(engine) as s:
        u = s.get(User, user_id)
        if not u:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": u.id, "email": u.email, "display_name": u.display_name}
