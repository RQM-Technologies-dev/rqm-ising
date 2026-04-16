"""Job management endpoints."""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from rqm_ising.schemas.common import make_error, make_success
from rqm_ising.schemas.jobs import JobListResponse
from rqm_ising.services.job_service import get_job_service
from rqm_ising.utils.ids import new_request_id

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
async def list_jobs(request: Request):
    """Return all jobs from the in-memory job store."""
    request_id = getattr(request.state, "request_id", new_request_id())
    jobs = get_job_service().list_all()
    data = JobListResponse(
        jobs=[j.model_dump() for j in jobs], total=len(jobs)
    ).model_dump()
    return make_success(data=data, request_id=request_id)


@router.get("/{job_id}")
async def get_job(job_id: str, request: Request):
    """Return a specific job by ID."""
    request_id = getattr(request.state, "request_id", new_request_id())
    job = get_job_service().get(job_id)
    if job is None:
        return JSONResponse(
            status_code=404,
            content=make_error(
                code="job_not_found",
                message=f"Job '{job_id}' not found.",
                request_id=request_id,
            ),
        )
    return make_success(data=job.model_dump(), request_id=request_id)
