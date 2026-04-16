"""
QEC workflow orchestration.

Coordinates provider calls, job lifecycle management, and artifact storage
for QEC-related operations. Provider selection happens through the registry.
"""

import logging

from rqm_ising.providers.registry import get_registry
from rqm_ising.schemas.jobs import JobType
from rqm_ising.schemas.qec import (
    QECBenchmarkRequest,
    QECBenchmarkRunResponse,
    QECDecodeRequest,
    QECDecodeSummary,
)
from rqm_ising.services.job_service import get_job_service

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
    return QECBenchmarkRunResponse(
        job_id=job.job_id,
        provider=response.provider,
        benchmark_id=response.benchmark_id,
        status=response.status,
    )
