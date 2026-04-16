"""Tests for /v1/providers endpoint and provider registry."""

from rqm_ising.providers.registry import get_registry


def test_providers_returns_200(client):
    response = client.get("/v1/providers")
    assert response.status_code == 200


def test_providers_envelope(client):
    data = client.get("/v1/providers").json()
    assert data["status"] == "success"
    assert "providers" in data["data"]
    assert "total" in data["data"]


def test_nvidia_ising_registered(client):
    data = client.get("/v1/providers").json()
    provider_ids = [p["name"] for p in data["data"]["providers"]]
    assert "nvidia_ising" in provider_ids


def test_nvidia_ising_capabilities(client):
    data = client.get("/v1/providers").json()
    nvidia = next(p for p in data["data"]["providers"] if p["name"] == "nvidia_ising")
    caps = nvidia["capabilities"]
    assert "calibration_analysis" in caps
    assert "qec_decoding" in caps
    assert nvidia["status"] in {"available", "unavailable"}
    assert nvidia["integration_mode"] in {"mock", "configured", "unavailable"}
    assert "summary" in nvidia


def test_provider_detail_returns_200(client):
    response = client.get("/v1/providers/nvidia_ising")
    assert response.status_code == 200


def test_provider_detail_payload(client):
    payload = client.get("/v1/providers/nvidia_ising").json()
    assert payload["status"] == "success"
    data = payload["data"]
    assert data["name"] == "nvidia_ising"
    assert data["display_name"] == "NVIDIA Ising"
    assert isinstance(data["capabilities"], list)
    assert isinstance(data["availability"], bool)
    assert isinstance(data["credentials_configured"], bool)
    assert isinstance(data["mock_only"], bool)
    assert data["integration_mode"] in {"mock", "configured", "unavailable"}
    assert "summary" in data


def test_provider_detail_not_found(client):
    response = client.get("/v1/providers/not-real")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "error"
    assert data["error"]["code"] == "provider_not_found"


def test_registry_get_nvidia_ising():
    provider = get_registry().get("nvidia_ising")
    assert provider is not None
    assert provider.provider_id == "nvidia_ising"


def test_registry_get_missing_returns_none():
    assert get_registry().get("nonexistent_provider") is None


def test_registry_get_or_raise_missing():
    import pytest
    with pytest.raises(ValueError, match="nonexistent_provider"):
        get_registry().get_or_raise("nonexistent_provider")
