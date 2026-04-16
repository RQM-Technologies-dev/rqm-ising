"""Calibration endpoints."""

import logging

from fastapi import APIRouter, Request

from rqm_ising.api.responses import error_response, success_response
from rqm_ising.schemas.calibration import CalibrationAnalyzeRequest, CalibrationRunRequest
from rqm_ising.workflows.calibration_workflow import analyze_calibration, submit_calibration_run

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/calibration", tags=["calibration"])


@router.post("/analyze")
async def calibration_analyze(body: CalibrationAnalyzeRequest, request: Request):
    """Analyze calibration experiment metadata and return a structured result."""
    try:
        result = analyze_calibration(body)
        return success_response(request, data=result.model_dump())
    except ValueError as exc:
        logger.warning(
            "Calibration analyze failed: request_id=%s error=%s",
            getattr(request.state, "request_id", "missing"),
            exc,
        )
        return error_response(
            request,
            code="provider_not_found",
            message="The requested provider is not registered.",
            status_code=404,
        )


@router.post("/run")
async def calibration_run(body: CalibrationRunRequest, request: Request):
    """Submit a calibration workflow job."""
    try:
        result = submit_calibration_run(body)
        return success_response(request, data=result.model_dump())
    except ValueError as exc:
        logger.warning(
            "Calibration run failed: request_id=%s error=%s",
            getattr(request.state, "request_id", "missing"),
            exc,
        )
        return error_response(
            request,
            code="provider_not_found",
            message="The requested provider is not registered.",
            status_code=404,
        )
