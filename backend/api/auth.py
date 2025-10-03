import os, datetime
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Request


pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = os.getenv("JWT_SECRET", "dev")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
JWT_TTL_MIN = int(os.getenv("JWT_TTL_MINUTES", "60"))

def hash_pw(pw: str) -> str:
    return pwd_ctx.hash(pw)

def verify_pw(pw: str, hashed: str) -> bool:
    return pwd_ctx.verify(pw, hashed)

def make_token(sub: str, minutes: int | None = None) -> str:
    ttl = minutes if minutes is not None else JWT_TTL_MIN
    now = datetime.datetime.utcnow()
    payload = {"sub": sub, "iat": now, "exp": now + datetime.timedelta(minutes=ttl)}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        return payload.get("sub")
    except JWTError:
        return None
