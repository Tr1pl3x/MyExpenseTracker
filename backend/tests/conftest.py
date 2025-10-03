# tests/conftest.py
import os
import sys
import uuid
import pathlib
import tempfile
import pytest

from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine

# --- Ensure backend root is importable
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# --- Create a unique temp directory + DB path per session
_TMP_DIR = pathlib.Path(tempfile.mkdtemp(prefix="exptrack_tests_"))
TEST_DB_PATH = _TMP_DIR / f"test_{uuid.uuid4().hex}.db"

# --- Test environment (set BEFORE importing app modules)
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH.as_posix()}"
os.environ["JWT_SECRET"] = "testsecret"
os.environ["APP_TZ"] = "UTC"
os.environ["ALLOWED_HOSTS"] = "testserver,localhost,127.0.0.1"
os.environ["FRONTEND_ORIGINS"] = "http://testserver"
os.environ["FORCE_HTTPS"] = "0"
os.environ["RATE_LIMIT_DEFAULT"] = "1000/minute"
os.environ["RATE_LIMIT_AUTH"] = "100/minute"
os.environ["RATE_LIMIT_WRITES"] = "100/minute"

# Now import the app
from api import db
from api.main import app
from api import models as _models  # ensure models registered

@pytest.fixture(scope="session")
def test_engine():
    """Create a throwaway SQLite engine and swap the app's engine to it."""
    engine = create_engine(
        os.environ["DATABASE_URL"],
        connect_args={"check_same_thread": False},  # needed for TestClient threads
    )
    db.engine = engine  # swap engine used by routes
    SQLModel.metadata.create_all(engine)
    yield engine
    # best-effort cleanup (Windows may keep handles briefly)
    try:
        engine.dispose()
    except Exception:
        pass
    try:
        TEST_DB_PATH.unlink(missing_ok=True)
    except Exception:
        pass
    try:
        _TMP_DIR.rmdir()
    except Exception:
        pass

@pytest.fixture()
def client(test_engine):
    with TestClient(app) as c:
        yield c

@pytest.fixture()
def auth_headers(client):
    """Create a fresh user and return Authorization headers."""
    email = f"u_{uuid.uuid4().hex[:8]}@test.com"
    payload = {"email": email, "password": "pw12345", "display_name": "Tester"}
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture()
def any_category_id(client, auth_headers):
    """Return an existing category id (defaults seeded on register)."""
    r = client.get("/categories", headers=auth_headers)
    assert r.status_code == 200, r.text
    cats = r.json()
    assert len(cats) >= 1
    return cats[0]["id"]
