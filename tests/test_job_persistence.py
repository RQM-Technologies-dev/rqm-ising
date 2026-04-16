"""Tests for persistent local job storage and restart-safe reload behavior."""

from rqm_ising.schemas.jobs import JobStatus, JobType
from rqm_ising.services.job_service import JobService
from rqm_ising.services.job_storage import JobStorage


def test_job_is_persisted_to_disk(tmp_path):
    storage = JobStorage(jobs_dir=str(tmp_path / "jobs"))
    service = JobService(storage=storage)

    job = service.create(JobType.calibration_workflow, "nvidia_ising", {"experiment_id": "exp-a"})

    expected_path = storage.jobs_dir / job.job_id / "job.json"
    assert expected_path.exists()


def test_persisted_jobs_reload_after_restart(tmp_path):
    jobs_dir = tmp_path / "jobs"
    storage = JobStorage(jobs_dir=str(jobs_dir))
    service_a = JobService(storage=storage)
    created = service_a.create(JobType.qec_benchmark, "nvidia_ising", {"benchmark_id": "bench-a"})
    service_a.update_status(
        created.job_id,
        JobStatus.completed,
        result_summary={"report_artifact": "/tmp/report.json"},
        artifact_paths=["/tmp/report.json"],
    )

    reloaded_storage = JobStorage(jobs_dir=str(jobs_dir))
    service_b = JobService(storage=reloaded_storage)
    loaded_count = service_b.load_persisted_jobs()
    loaded = service_b.get(created.job_id)

    assert loaded_count >= 1
    assert loaded is not None
    assert loaded.status == JobStatus.completed
    assert loaded.result_summary is not None
    assert loaded.result_summary["report_artifact"] == "/tmp/report.json"
