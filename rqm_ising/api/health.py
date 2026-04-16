"""Health check endpoint."""

from fastapi import APIRouter, Request

from rqm_ising.api.responses import success_response

router = APIRouter(tags=["meta"])


@router.get("/health")
async def health(request: Request):
    return success_response(request, data={"healthy": True})
