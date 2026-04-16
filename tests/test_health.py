"""Tests for /health and /version endpoints."""


def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_envelope(client):
    data = client.get("/health").json()
    assert data["status"] == "success"
    assert data["data"]["healthy"] is True
    assert "request_id" in data["meta"]


def test_version_returns_200(client):
    response = client.get("/version")
    assert response.status_code == 200


def test_version_field(client):
    data = client.get("/version").json()
    assert "version" in data
    assert data["version"] == "0.1.0"
