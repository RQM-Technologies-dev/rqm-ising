"""
Calibration workflow orchestration.

Coordinates provider calls, job lifecycle management, and artifact storage
for calibration-related operations. Provider selection happens through the
registry — this module does not import provider-specific code directly.
"""

import logging

from rqm_ising.providers.registry import get_registry
from rqm_ising.schemas.benchmarks import BenchmarkArtifact
from rqm_ising.schemas.calibration import (
    CalibrationAnalysisResult,
    CalibrationAnalyzeRequest,
    CalibrationRunRequest,
    CalibrationRunResponse,
)
from rqm_ising.schemas.jobs import JobStatus, JobType
from rqm_ising.services.artifact_service import get_artifact_service
from rqm_ising.services.job_service import get_job_service
from rqm_ising.utils.ids import new_id

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
    report_payload = {
        "report_id": f"cal_report_{new_id()[:8]}",
        "benchmark_type": "calibration",
        "provider": request.provider,
        "experiment_type": request.workflow_params.get("experiment_type", "gate_calibration"),
        "experiment_id": request.experiment_id,
        "drift_indicators": {
            "frequency_drift_hz": 220.0,
            "amplitude_drift_pct": 0.8,
            "phase_drift_deg": 1.2,
        },
        "visual_findings": [
            "Rabi oscillation fit remains stable across the central qubit cluster.",
            "Slight coherence drift observed on edge qubits in the final window.",
        ],
        "recommended_actions": [
            "Re-run Ramsey sequence for qubits with elevated phase drift.",
            "Schedule recalibration before next high-depth workload.",
        ],
        "confidence": 0.79,
        "notes": [
            "Mock calibration report generated for local workflow validation.",
            "Replace with provider-backed analysis in external mode.",
        ],
    }
    artifact_path = get_artifact_service().write_json(
        data=report_payload,
        filename="calibration_report.json",
        sub_path=f"jobs/{job.job_id}",
    )
    artifact = BenchmarkArtifact(
        path=str(artifact_path),
        kind="calibration_report",
        format="json",
        label="Calibration run report",
    )
    result_summary = {
        "report_artifact": artifact.path,
        "report_type": artifact.kind,
        "summary": "Calibration workflow completed with structured report artifact output.",
    }
    job_service.update_status(
        job.job_id,
        JobStatus.completed,
        result_summary=result_summary,
        artifact_paths=[artifact.path],
    )
    logger.info("Calibration artifact written: job_id=%s path=%s", job.job_id, artifact.path)
    # Update the response to use the job_id from our job service
    return CalibrationRunResponse(
        job_id=job.job_id,
        provider=response.provider,
        experiment_id=response.experiment_id,
        status=JobStatus.completed.value,
        artifact_paths=[artifact.path],
        result_summary=result_summary,
    )
