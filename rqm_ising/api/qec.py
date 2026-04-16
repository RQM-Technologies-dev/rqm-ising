"""QEC endpoints."""

import logging

from fastapi import APIRouter, Request

from rqm_ising.api.responses import error_response, success_response
from rqm_ising.schemas.qec import QECBenchmarkRequest, QECDecodeRequest
from rqm_ising.workflows.qec_workflow import decode_syndromes, submit_qec_benchmark

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/qec", tags=["qec"])


@router.post("/decode")
async def qec_decode(body: QECDecodeRequest, request: Request):
    """Decode syndrome data via the requested provider."""
    try:
        result = decode_syndromes(body)
        return success_response(request, result.model_dump())
    except ValueError as exc:
        logger.warning(
            "QEC decode failed: request_id=%s error=%s",
            getattr(request.state, "request_id", "missing"),
            exc,
        )
        return error_response(
            request,
            code="provider_not_found",
            message="The requested provider is not registered.",
            status_code=404,
        )


@router.post("/benchmark")
async def qec_benchmark(body: QECBenchmarkRequest, request: Request):
    """Submit a QEC benchmark job comparing decoder approaches."""
    try:
        result = submit_qec_benchmark(body)
        return success_response(request, result.model_dump())
    except ValueError as exc:
        logger.warning(
            "QEC benchmark failed: request_id=%s error=%s",
            getattr(request.state, "request_id", "missing"),
            exc,
        )
        return error_response(
            request,
            code="provider_not_found",
            message="The requested provider is not registered.",
            status_code=404,
        )
