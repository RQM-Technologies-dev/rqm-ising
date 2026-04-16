"""Tests for /v1/calibration/analyze and /v1/calibration/run endpoints."""

ANALYZE_PAYLOAD = {
    "experiment_id": "test-exp-001",
    "qubit_count": 4,
    "coupling_map": [[0, 1], [1, 2], [2, 3]],
    "gate_set": ["cx", "h", "rz"],
    "noise_metadata": {},
    "provider": "nvidia_ising",
}

RUN_PAYLOAD = {
    "experiment_id": "test-exp-002",
    "qubit_count": 4,
    "coupling_map": [[0, 1], [1, 2], [2, 3]],
    "gate_set": ["cx", "h"],
    "workflow_params": {},
    "provider": "nvidia_ising",
}


def test_calibration_analyze_returns_200(client):
    response = client.post("/v1/calibration/analyze", json=ANALYZE_PAYLOAD)
    assert response.status_code == 200


def test_calibration_analyze_envelope(client):
    data = client.post("/v1/calibration/analyze", json=ANALYZE_PAYLOAD).json()
    assert data["status"] == "success"
    assert "experiment_id" in data["data"]
    assert data["data"]["experiment_id"] == "test-exp-001"
    assert data["data"]["provider"] == "nvidia_ising"
    assert data["data"]["qubit_count"] == 4


def test_calibration_analyze_has_gate_fidelities(client):
    data = client.post("/v1/calibration/analyze", json=ANALYZE_PAYLOAD).json()
    assert "recommended_gate_fidelities" in data["data"]
    fidelities = data["data"]["recommended_gate_fidelities"]
    assert isinstance(fidelities, dict)
    assert len(fidelities) > 0


def test_calibration_analyze_has_t1_t2(client):
    data = client.post("/v1/calibration/analyze", json=ANALYZE_PAYLOAD).json()
    assert "t1_estimates_us" in data["data"]
    assert "t2_estimates_us" in data["data"]


def test_calibration_analyze_stub_warning(client):
    data = client.post("/v1/calibration/analyze", json=ANALYZE_PAYLOAD).json()
    # In stub mode, a warning should be present
    warnings = data["data"].get("analysis_warnings", [])
    assert any("stub" in w.lower() for w in warnings)


def test_calibration_analyze_unknown_provider(client):
    payload = {**ANALYZE_PAYLOAD, "provider": "unknown_provider"}
    data = client.post("/v1/calibration/analyze", json=payload).json()
    assert data["status"] == "error"
    assert data["error"]["code"] == "provider_not_found"


def test_calibration_run_returns_200(client):
    response = client.post("/v1/calibration/run", json=RUN_PAYLOAD)
    assert response.status_code == 200


def test_calibration_run_envelope(client):
    data = client.post("/v1/calibration/run", json=RUN_PAYLOAD).json()
    assert data["status"] == "success"
    assert "job_id" in data["data"]
    assert data["data"]["job_id"].startswith("job_")
    assert data["data"]["status"] == "completed"
    assert data["data"]["artifact_paths"]
    assert data["data"]["artifact_paths"][0].endswith("/calibration_report.json")
    assert "report_artifact" in data["data"]["result_summary"]
