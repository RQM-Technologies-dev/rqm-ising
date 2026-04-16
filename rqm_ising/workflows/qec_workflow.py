"""
QEC workflow orchestration.

Coordinates provider calls, job lifecycle management, and artifact storage
for QEC-related operations. Provider selection happens through the registry.
"""

import logging

from rqm_ising.providers.registry import get_registry
from rqm_ising.schemas.benchmarks import BenchmarkComparison, BenchmarkMetric, BenchmarkSummary
from rqm_ising.schemas.jobs import JobStatus, JobType
from rqm_ising.schemas.qec import (
    QECBenchmarkRequest,
    QECBenchmarkRunResponse,
    QECDecodeRequest,
    QECDecodeSummary,
)
from rqm_ising.services.artifact_service import get_artifact_service
from rqm_ising.services.job_service import get_job_service
from rqm_ising.utils.ids import new_id
from rqm_ising.utils.timestamps import utcnow_iso

logger = logging.getLogger(__name__)


def decode_syndromes(request: QECDecodeRequest) -> QECDecodeSummary:
    """
    Decode syndrome data through the requested provider.

    This is a synchronous operation — it returns a result immediately.
    """
    provider = get_registry().get_or_raise(request.provider)
    logger.info(
        "Running QEC decode: run_id=%s code=%s d=%d provider=%s",
        request.run_id,
        request.code_type,
        request.distance,
        request.provider,
    )
    return provider.run_qec_decoding(request)


def submit_qec_benchmark(request: QECBenchmarkRequest) -> QECBenchmarkRunResponse:
    """
    Submit a QEC benchmark job through the requested provider.

    Creates a job record in the job service so the caller can track progress
    via /v1/jobs/{job_id}.
    """
    provider = get_registry().get_or_raise(request.provider)
    job_service = get_job_service()

    job = job_service.create(
        job_type=JobType.qec_benchmark,
        provider=request.provider,
        input_summary={
            "benchmark_id": request.benchmark_id,
            "code_type": request.code_type,
            "distance": request.distance,
            "decoders": request.decoders,
        },
    )

    logger.info(
        "Submitting QEC benchmark: job_id=%s benchmark_id=%s provider=%s",
        job.job_id,
        request.benchmark_id,
        request.provider,
    )

    response = provider.run_qec_benchmark(request)
    artifact_service = get_artifact_service()
    benchmark_report = {
        "report_id": f"qec_benchmark_{new_id()[:8]}",
        "benchmark_type": "qec_benchmark",
        "provider": request.provider,
        "created_at": utcnow_iso(),
        "summary": BenchmarkSummary(
            headline=f"QEC benchmark submitted for {request.code_type} d={request.distance}",
            key_findings=[
                "Mock benchmark output generated for workflow integration.",
                "Candidate decoder metrics are illustrative and not hardware measured.",
            ],
        ).model_dump(),
        "comparisons": [
            BenchmarkComparison(
                decoder_baseline=request.decoders[0],
                decoder_candidate=request.decoders[-1],
                logical_error_rate=0.0016,
                syndrome_density_reduction=0.21,
                estimated_latency_ms=1.6,
                confidence=0.72,
                notes="Mock values generated at workflow completion.",
            ).model_dump()
        ],
        "metrics": [
            BenchmarkMetric(
                name="logical_error_rate",
                value=0.0016,
                unit="ratio",
                direction="lower_is_better",
                notes="Mock logical error rate from benchmark flow.",
            ).model_dump(),
            BenchmarkMetric(
                name="syndrome_density_reduction",
                value=0.21,
                unit="ratio",
                direction="higher_is_better",
                notes="Mock reduction against baseline decoder.",
            ).model_dump(),
            BenchmarkMetric(
                name="estimated_latency_ms",
                value=1.6,
                unit="ms",
                direction="lower_is_better",
                notes="Mock latency estimate for candidate decoder.",
            ).model_dump(),
        ],
        "recommended_next_step": (
            "Replay this benchmark with provider-backed syndrome traces and compare confidence."
        ),
        "notes": [
            "Generated in mock integration mode.",
            "Workflow-attached benchmark artifact for Studio consumption.",
        ],
    }
    artifact_path = artifact_service.write_json(
        data=benchmark_report,
        filename="benchmark_report.json",
        sub_path=f"jobs/{job.job_id}",
    )
    result_summary = {
        "message": "QEC benchmark completed with Studio-ready benchmark artifact.",
        "benchmark_report_path": str(artifact_path),
        "provider_status": "mock_mode" if not provider.externally_connected else "configured",
        "benchmark_id": request.benchmark_id,
    }
    job_service.update_status(
        job_id=job.job_id,
        status=JobStatus.completed,
        result_summary=result_summary,
        artifact_paths=[str(artifact_path)],
    )
    logger.info(
        "QEC benchmark artifact generated: job_id=%s path=%s",
        job.job_id,
        artifact_path,
    )
    return QECBenchmarkRunResponse(
        job_id=job.job_id,
        provider=response.provider,
        benchmark_id=response.benchmark_id,
        status=JobStatus.completed.value,
        artifact_paths=[str(artifact_path)],
        result_summary=result_summary,
    )
