"""QEC endpoints."""

import logging

from fastapi import APIRouter, Request

from rqm_ising.schemas.common import make_error, make_success
from rqm_ising.schemas.qec import QECBenchmarkRequest, QECDecodeRequest
from rqm_ising.utils.ids import new_request_id
from rqm_ising.workflows.qec_workflow import decode_syndromes, submit_qec_benchmark

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/qec", tags=["qec"])


@router.post("/decode")
async def qec_decode(body: QECDecodeRequest, request: Request):
    """Decode syndrome data via the requested provider."""
    request_id = getattr(request.state, "request_id", new_request_id())
    try:
        result = decode_syndromes(body)
        return make_success(data=result.model_dump(), request_id=request_id)
    except ValueError as exc:
        logger.warning("QEC decode failed: %s", exc)
        return make_error(
            code="provider_not_found",
            message="The requested provider is not registered.",
            request_id=request_id,
        )


@router.post("/benchmark")
async def qec_benchmark(body: QECBenchmarkRequest, request: Request):
    """Submit a QEC benchmark job comparing decoder approaches."""
    request_id = getattr(request.state, "request_id", new_request_id())
    try:
        result = submit_qec_benchmark(body)
        return make_success(data=result.model_dump(), request_id=request_id)
    except ValueError as exc:
        logger.warning("QEC benchmark failed: %s", exc)
        return make_error(
            code="provider_not_found",
            message="The requested provider is not registered.",
            request_id=request_id,
        )
