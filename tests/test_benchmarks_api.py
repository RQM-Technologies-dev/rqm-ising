"""Tests for /v1/benchmarks/report endpoint."""


def test_benchmark_report_returns_200(client):
    response = client.get("/v1/benchmarks/report")
    assert response.status_code == 200


def test_benchmark_report_shape(client):
    payload = client.get("/v1/benchmarks/report").json()
    assert payload["status"] == "success"
    data = payload["data"]
    assert data["report_id"].startswith("report_")
    assert "benchmark_type" in data
    assert "provider" in data
    assert "created_at" in data
    assert "summary" in data
    assert "comparisons" in data
    assert "metrics" in data
    assert "artifact_paths" in data
    assert "recommended_next_step" in data
    assert "notes" in data
    assert isinstance(data["artifact_paths"], list)
