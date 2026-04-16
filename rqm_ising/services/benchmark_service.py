"""
Benchmark service — orchestrates benchmark report generation and storage.
"""

import logging

from rqm_ising.schemas.benchmarks import BenchmarkReport, DecoderBenchmarkEntry
from rqm_ising.services.artifact_service import get_artifact_service
from rqm_ising.utils.ids import new_id

logger = logging.getLogger(__name__)


class BenchmarkService:
    def __init__(self) -> None:
        self._artifact_service = get_artifact_service()

    def generate_mock_report(
        self,
        code_type: str = "surface_code",
        distance: int = 5,
        provider: str = "nvidia_ising",
    ) -> BenchmarkReport:
        """
        Generate a mock benchmark report and persist it as a JSON artifact.

        In Phase 2, this will be replaced by real benchmark job results
        retrieved from the job service after a benchmark run completes.
        """
        report_id = f"report_{new_id()[:8]}"
        entries = [
            DecoderBenchmarkEntry(
                decoder="mwpm",
                logical_error_rate=0.0012,
                avg_decode_time_ms=4.2,
                rounds_tested=1000,
            ),
            DecoderBenchmarkEntry(
                decoder="union_find",
                logical_error_rate=0.0018,
                avg_decode_time_ms=1.8,
                rounds_tested=1000,
            ),
        ]
        report = BenchmarkReport(
            report_id=report_id,
            code_type=code_type,
            distance=distance,
            provider=provider,
            entries=entries,
            summary=(
                f"Mock benchmark report for {code_type} d={distance} via {provider}. "
                "Results are illustrative — replace with real benchmark data in Phase 2."
            ),
        )

        try:
            artifact_path = self._artifact_service.write_json(
                data=report.model_dump(),
                filename=f"{report_id}.json",
                sub_path="benchmarks",
            )
            report = report.model_copy(update={"artifact_path": str(artifact_path)})
        except Exception:
            logger.exception("Failed to write benchmark artifact; continuing without artifact.")

        return report


_benchmark_service = BenchmarkService()


def get_benchmark_service() -> BenchmarkService:
    return _benchmark_service
