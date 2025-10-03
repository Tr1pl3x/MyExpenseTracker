# tests/test_auth.py
import uuid

def test_register_login_me(client):
    email = f"me_{uuid.uuid4().hex[:8]}@test.com"  # <- unique per run
    # register
    r1 = client.post("/auth/register", json={"email": email, "password": "pw123", "display_name": "Me"})
    assert r1.status_code == 200
    token = r1.json()["access_token"]

    # me
    r2 = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    assert r2.json()["email"] == email

    # login
    r3 = client.post("/auth/login", json={"email": email, "password": "pw123"})
    assert r3.status_code == 200
    assert "access_token" in r3.json()
