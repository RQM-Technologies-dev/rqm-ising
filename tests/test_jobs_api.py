"""Tests for /v1/jobs and /v1/jobs/{job_id} endpoints."""

CALIBRATION_RUN_PAYLOAD = {
    "experiment_id": "jobs-test-exp",
    "qubit_count": 2,
    "coupling_map": [[0, 1]],
    "gate_set": ["cx"],
    "workflow_params": {},
    "provider": "nvidia_ising",
}


def _create_job(client) -> str:
    """Helper: create a calibration run job and return its job_id."""
    data = client.post("/v1/calibration/run", json=CALIBRATION_RUN_PAYLOAD).json()
    assert data["status"] == "success"
    return data["data"]["job_id"]


def test_list_jobs_returns_200(client):
    response = client.get("/v1/jobs")
    assert response.status_code == 200


def test_list_jobs_envelope(client):
    data = client.get("/v1/jobs").json()
    assert data["status"] == "success"
    assert "jobs" in data["data"]
    assert "total" in data["data"]


def test_job_appears_in_list_after_creation(client):
    job_id = _create_job(client)
    data = client.get("/v1/jobs").json()
    job_ids = [j["job_id"] for j in data["data"]["jobs"]]
    assert job_id in job_ids


def test_get_job_returns_200(client):
    job_id = _create_job(client)
    response = client.get(f"/v1/jobs/{job_id}")
    assert response.status_code == 200


def test_get_job_fields(client):
    job_id = _create_job(client)
    data = client.get(f"/v1/jobs/{job_id}").json()
    assert data["status"] == "success"
    job = data["data"]
    assert job["job_id"] == job_id
    assert job["status"] == "completed"
    assert job["provider"] == "nvidia_ising"
    assert job["artifact_paths"]
    assert job["artifact_paths"][0].endswith("/calibration_report.json")
    assert "report_artifact" in job["result_summary"]
    assert "created_at" in job
    assert "updated_at" in job


def test_get_job_not_found(client):
    response = client.get("/v1/jobs/job_doesnotexist")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "error"
    assert data["error"]["code"] == "job_not_found"
