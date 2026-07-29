"""Tests for /health and /version endpoints."""

from rqm_ising import __version__


def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_envelope(client):
    data = client.get("/health").json()
    assert data["status"] == "success"
    assert data["data"]["healthy"] is True
    assert "request_id" in data["meta"]
    assert "processing_time_ms" in data["meta"]


def test_version_returns_200(client):
    response = client.get("/version")
    assert response.status_code == 200


def test_version_envelope(client):
    data = client.get("/version").json()
    assert data["status"] == "success"
    assert data["data"]["version"] == __version__
    assert "request_id" in data["meta"]
    assert "processing_time_ms" in data["meta"]
