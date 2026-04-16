"""
Benchmark workflow orchestration.

Orchestrates benchmark report generation. In Phase 2 this will coordinate
benchmark job submissions and wait for completion before generating reports.
"""

import logging

from rqm_ising.schemas.benchmarks import BenchmarkReport
from rqm_ising.services.benchmark_service import get_benchmark_service

logger = logging.getLogger(__name__)


def generate_benchmark_report(
    code_type: str = "surface_code",
    distance: int = 5,
    provider: str = "nvidia_ising",
) -> BenchmarkReport:
    """
    Generate and persist a benchmark report.

    Phase 1: returns a mock report with illustrative data.
    Phase 2: retrieves real benchmark data from completed jobs.
    """
    logger.info(
        "Generating benchmark report: code=%s d=%d provider=%s",
        code_type,
        distance,
        provider,
    )
    return get_benchmark_service().generate_mock_report(
        code_type=code_type,
        distance=distance,
        provider=provider,
    )
