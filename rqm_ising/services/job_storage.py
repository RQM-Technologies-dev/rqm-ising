"""Filesystem-backed persistence helper for workflow jobs."""

from pathlib import Path

from rqm_ising.config import get_settings
from rqm_ising.schemas.jobs import Job
from rqm_ising.storage.filesystem import list_files, read_json_file, write_json_file


class JobStorage:
    """Read/write Job records under artifacts/jobs/{job_id}/job.json."""

    def __init__(self, jobs_dir: str | None = None) -> None:
        settings = get_settings()
        self._jobs_dir = Path(jobs_dir or settings.jobs_dir).resolve()

    @property
    def jobs_dir(self) -> Path:
        return self._jobs_dir

    def ensure_dirs(self) -> Path:
        self._jobs_dir.mkdir(parents=True, exist_ok=True)
        return self._jobs_dir

    def save_job(self, job: Job) -> Path:
        """Persist a job snapshot to artifacts/jobs/{job_id}/job.json."""
        target = self._jobs_dir / job.job_id / "job.json"
        write_json_file(target, job.model_dump(mode="json"))
        return target

    def load_jobs(self) -> list[Job]:
        """Load all persisted jobs from disk."""
        self.ensure_dirs()
        files = list_files(self._jobs_dir, "*/job.json")
        loaded: list[Job] = []
        for file_path in files:
            payload = read_json_file(file_path)
            loaded.append(Job.model_validate(payload))
        return loaded

