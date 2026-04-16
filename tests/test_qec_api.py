"""Tests for /v1/qec/decode and /v1/qec/benchmark endpoints."""

DECODE_PAYLOAD = {
    "run_id": "test-run-001",
    "code_type": "surface_code",
    "distance": 5,
    "syndrome_data": [[0, 1, 0, 1], [1, 0, 1, 0], [0, 0, 1, 1]],
    "decoder": "mwpm",
    "provider": "nvidia_ising",
}

BENCHMARK_PAYLOAD = {
    "benchmark_id": "test-bench-001",
    "code_type": "surface_code",
    "distance": 5,
    "decoders": ["mwpm", "union_find"],
    "rounds": 500,
    "provider": "nvidia_ising",
}


def test_qec_decode_returns_200(client):
    response = client.post("/v1/qec/decode", json=DECODE_PAYLOAD)
    assert response.status_code == 200


def test_qec_decode_envelope(client):
    data = client.post("/v1/qec/decode", json=DECODE_PAYLOAD).json()
    assert data["status"] == "success"
    assert data["data"]["run_id"] == "test-run-001"
    assert data["data"]["provider"] == "nvidia_ising"
    assert data["data"]["code_type"] == "surface_code"
    assert data["data"]["distance"] == 5
    assert data["data"]["decoder"] == "mwpm"


def test_qec_decode_has_logical_error_rate(client):
    data = client.post("/v1/qec/decode", json=DECODE_PAYLOAD).json()
    ler = data["data"]["logical_error_rate"]
    assert isinstance(ler, float)
    assert 0.0 <= ler <= 1.0


def test_qec_decode_rounds_processed(client):
    data = client.post("/v1/qec/decode", json=DECODE_PAYLOAD).json()
    assert data["data"]["rounds_processed"] == len(DECODE_PAYLOAD["syndrome_data"])


def test_qec_decode_unknown_provider(client):
    payload = {**DECODE_PAYLOAD, "provider": "unknown_provider"}
    data = client.post("/v1/qec/decode", json=payload).json()
    assert data["status"] == "error"
    assert data["error"]["code"] == "provider_not_found"


def test_qec_benchmark_returns_200(client):
    response = client.post("/v1/qec/benchmark", json=BENCHMARK_PAYLOAD)
    assert response.status_code == 200


def test_qec_benchmark_envelope(client):
    data = client.post("/v1/qec/benchmark", json=BENCHMARK_PAYLOAD).json()
    assert data["status"] == "success"
    assert "job_id" in data["data"]
    assert data["data"]["job_id"].startswith("job_")
    assert data["data"]["status"] == "completed"
    assert data["data"]["artifact_paths"]
    assert data["data"]["artifact_paths"][0].endswith("/benchmark_report.json")
    assert "benchmark_report_path" in data["data"]["result_summary"]
