from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_with_valid_credentials_returns_token():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "admin123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_with_invalid_credentials_returns_401():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "wrong_password"},
    )

    assert response.status_code == 401


def get_admin_token() -> str:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "admin123"},
    )
    return response.json()["access_token"]
