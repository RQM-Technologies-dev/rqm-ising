"""Calibration endpoints."""

import logging

from fastapi import APIRouter, Request

from rqm_ising.schemas.calibration import CalibrationAnalyzeRequest, CalibrationRunRequest
from rqm_ising.schemas.common import make_error, make_success
from rqm_ising.utils.ids import new_request_id
from rqm_ising.workflows.calibration_workflow import analyze_calibration, submit_calibration_run

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/calibration", tags=["calibration"])


@router.post("/analyze")
async def calibration_analyze(body: CalibrationAnalyzeRequest, request: Request):
    """Analyze calibration experiment metadata and return a structured result."""
    request_id = getattr(request.state, "request_id", new_request_id())
    try:
        result = analyze_calibration(body)
        return make_success(data=result.model_dump(), request_id=request_id)
    except ValueError as exc:
        logger.warning("Calibration analyze failed: %s", exc)
        return make_error(
            code="provider_not_found",
            message="The requested provider is not registered.",
            request_id=request_id,
        )


@router.post("/run")
async def calibration_run(body: CalibrationRunRequest, request: Request):
    """Submit a calibration workflow job."""
    request_id = getattr(request.state, "request_id", new_request_id())
    try:
        result = submit_calibration_run(body)
        return make_success(data=result.model_dump(), request_id=request_id)
    except ValueError as exc:
        logger.warning("Calibration run failed: %s", exc)
        return make_error(
            code="provider_not_found",
            message="The requested provider is not registered.",
            request_id=request_id,
        )
