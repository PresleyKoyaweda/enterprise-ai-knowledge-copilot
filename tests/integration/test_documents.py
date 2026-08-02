from fastapi.testclient import TestClient

from app.main import app
from tests.integration.test_auth import get_admin_token

client = TestClient(app)


def test_upload_document_without_token_returns_401():
    response = client.post(
        "/api/v1/documents", files={"file": ("test.txt", b"contenu", "text/plain")}
    )

    assert response.status_code == 401


def test_upload_document_with_invalid_token_returns_401():
    headers = {"Authorization": "Bearer token_invalide_falsifie"}
    response = client.post(
        "/api/v1/documents",
        files={"file": ("test.txt", b"contenu", "text/plain")},
        headers=headers,
    )

    assert response.status_code == 401


def test_upload_unsupported_format_returns_400():
    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/v1/documents",
        files={"file": ("test.png", b"fake image content", "image/png")},
        headers=headers,
    )

    assert response.status_code == 400
