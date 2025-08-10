import uuid

import pytest
from fastapi.testclient import TestClient

from main import app  # type: ignore


@pytest.fixture(scope="module")
def client():
    # Using context manager ensures FastAPI lifespan (table creation in dev) runs
    with TestClient(app) as c:
        yield c


def test_root_health(client):
    # Expect 404 because no root route; ensures app boots
    response = client.get("/")
    assert response.status_code in (404, 200)


def test_auth_signup_and_login_flow(client):
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    payload = {"email": unique_email, "full_name": "Test User", "password": "secret123"}
    r = client.post("/api/v1/auth/signup", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["email"] == unique_email
    assert "session_id" in r.cookies

    me = client.get("/api/v1/auth/me")
    assert me.status_code == 200
    body = me.json()
    assert body["authenticated"] is True
    assert body["user"]["email"] == unique_email

    form = {"username": unique_email, "password": payload["password"]}
    r2 = client.post("/api/v1/auth/login", data=form)
    assert r2.status_code == 200
    assert r2.json()["email"] == unique_email
    assert "session_id" in r2.cookies


def test_logout_revokes_session(client):
    import uuid

    email = f"logout_{uuid.uuid4().hex[:8]}@example.com"
    payload = {"email": email, "full_name": "Logout Test", "password": "secret123"}
    r = client.post("/api/v1/auth/signup", json=payload)
    assert r.status_code == 201
    assert "session_id" in r.cookies
    me_before = client.get("/api/v1/auth/me")
    assert me_before.status_code == 200 and me_before.json()["authenticated"]
    out = client.post("/api/v1/auth/logout")
    assert out.status_code == 200
    me_after = client.get("/api/v1/auth/me")
    assert me_after.status_code == 200
    assert me_after.json() == {"authenticated": False, "user": None}
