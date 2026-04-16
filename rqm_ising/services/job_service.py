"""
In-memory job service.

Manages the lifecycle of async workflow jobs. This implementation uses a
thread-safe in-memory store. The interface is designed so the backing store
can be replaced with a database implementation without changing callers.
"""

import threading

from rqm_ising.schemas.jobs import Job, JobStatus, JobType
from rqm_ising.utils.ids import new_job_id
from rqm_ising.utils.timestamps import utcnow


class JobService:
    """CRUD operations for workflow jobs, backed by an in-memory dictionary."""

    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()

    def create(
        self,
        job_type: JobType,
        provider: str,
        input_summary: dict | None = None,
    ) -> Job:
        """Create and persist a new job in pending status."""
        now = utcnow()
        job = Job(
            job_id=new_job_id(),
            type=job_type,
            status=JobStatus.pending,
            provider=provider,
            input_summary=input_summary or {},
            artifact_paths=[],
            result_summary=None,
            created_at=now,
            updated_at=now,
        )
        with self._lock:
            self._jobs[job.job_id] = job
        return job

    def get(self, job_id: str) -> Job | None:
        """Return the job with the given ID, or None if not found."""
        with self._lock:
            return self._jobs.get(job_id)

    def list_all(self) -> list[Job]:
        """Return all jobs, sorted by creation time descending."""
        with self._lock:
            return sorted(self._jobs.values(), key=lambda j: j.created_at, reverse=True)

    def update_status(
        self,
        job_id: str,
        status: JobStatus,
        result_summary: dict | None = None,
        artifact_paths: list[str] | None = None,
    ) -> Job | None:
        """Update the status (and optionally results) of an existing job."""
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return None
            updated = job.model_copy(
                update={
                    "status": status,
                    "updated_at": utcnow(),
                    **({"result_summary": result_summary} if result_summary is not None else {}),
                    **({"artifact_paths": artifact_paths} if artifact_paths is not None else {}),
                }
            )
            self._jobs[job_id] = updated
            return updated


# Module-level singleton — suitable for the current in-memory implementation.
# Replace with dependency injection if/when a database backend is introduced.
_job_service = JobService()


def get_job_service() -> JobService:
    return _job_service
