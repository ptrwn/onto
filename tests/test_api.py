import os

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_foo_without_token():
    os.environ["API_TOKEN"] = "test-token"

    response = client.get("/foo")

    assert response.status_code == 401


def test_foo_with_invalid_token():
    os.environ["API_TOKEN"] = "test-token"

    response = client.get(
        "/foo",
        headers={"Authorization": "Bearer wrong-token"},
    )

    assert response.status_code == 401


def test_foo_with_valid_token():
    os.environ["API_TOKEN"] = "test-token"

    response = client.get(
        "/foo",
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == 200
    assert response.json() == "bar"
