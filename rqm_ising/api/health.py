"""Health check endpoint."""

from fastapi import APIRouter, Request

from rqm_ising.utils.ids import new_request_id

router = APIRouter(tags=["meta"])


@router.get("/health")
async def health(request: Request):
    request_id = getattr(request.state, "request_id", new_request_id())
    return {
        "status": "success",
        "data": {"healthy": True},
        "meta": {"request_id": request_id, "processing_time_ms": None},
    }
