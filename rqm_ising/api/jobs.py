"""Job management endpoints."""

from fastapi import APIRouter, Request

from rqm_ising.api.responses import error_response, success_response
from rqm_ising.schemas.jobs import JobListResponse
from rqm_ising.services.job_service import get_job_service

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
async def list_jobs(request: Request):
    """Return all jobs from local persistent job storage."""
    jobs = get_job_service().list_all()
    data = JobListResponse(
        jobs=[j.model_dump() for j in jobs], total=len(jobs)
    ).model_dump()
    return success_response(request, data=data)


@router.get("/{job_id}")
async def get_job(job_id: str, request: Request):
    """Return a specific job by ID."""
    job = get_job_service().get(job_id)
    if job is None:
        return error_response(
            request,
            status_code=404,
            code="job_not_found",
            message=f"Job '{job_id}' not found.",
        )
    return success_response(request, data=job.model_dump())
