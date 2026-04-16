"""
Calibration workflow orchestration.

Coordinates provider calls, job lifecycle management, and artifact storage
for calibration-related operations. Provider selection happens through the
registry — this module does not import provider-specific code directly.
"""

import logging

from rqm_ising.providers.registry import get_registry
from rqm_ising.schemas.calibration import (
    CalibrationAnalysisResult,
    CalibrationAnalyzeRequest,
    CalibrationRunRequest,
    CalibrationRunResponse,
)
from rqm_ising.schemas.jobs import JobType
from rqm_ising.services.job_service import get_job_service

logger = logging.getLogger(__name__)


def analyze_calibration(request: CalibrationAnalyzeRequest) -> CalibrationAnalysisResult:
    """
    Run a calibration analysis through the requested provider.

    This is a synchronous operation — it returns a result immediately
    without creating a persistent job record.
    """
    provider = get_registry().get_or_raise(request.provider)
    logger.info(
        "Running calibration analysis: experiment=%s provider=%s",
        request.experiment_id,
        request.provider,
    )
    return provider.run_calibration_analysis(request)


def submit_calibration_run(request: CalibrationRunRequest) -> CalibrationRunResponse:
    """
    Submit a calibration workflow job through the requested provider.

    Creates a job record in the job service so the caller can track progress
    via /v1/jobs/{job_id}.
    """
    provider = get_registry().get_or_raise(request.provider)
    job_service = get_job_service()

    # Create job record before submitting to provider
    job = job_service.create(
        job_type=JobType.calibration_workflow,
        provider=request.provider,
        input_summary={
            "experiment_id": request.experiment_id,
            "qubit_count": request.qubit_count,
        },
    )

    logger.info(
        "Submitting calibration workflow: job_id=%s experiment=%s provider=%s",
        job.job_id,
        request.experiment_id,
        request.provider,
    )

    response = provider.run_calibration_workflow(request)
    # Update the response to use the job_id from our job service
    return CalibrationRunResponse(
        job_id=job.job_id,
        provider=response.provider,
        experiment_id=response.experiment_id,
        status=response.status,
    )
