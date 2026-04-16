"""
Benchmark service — orchestrates benchmark report generation and storage.
"""

import logging

from rqm_ising.schemas.benchmarks import (
    BenchmarkArtifact,
    BenchmarkComparison,
    BenchmarkMetric,
    BenchmarkReport,
    BenchmarkSummary,
)
from rqm_ising.services.artifact_service import get_artifact_service
from rqm_ising.utils.ids import new_id
from rqm_ising.utils.timestamps import utcnow

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
        comparison = BenchmarkComparison(
            decoder_baseline="mwpm",
            decoder_candidate="union_find",
            logical_error_rate=0.0018,
            syndrome_density_reduction=0.17,
            estimated_latency_ms=1.8,
            confidence=0.74,
            notes="Mock comparison values for Studio integration prototyping.",
        )
        metrics = [
            BenchmarkMetric(
                name="decoder_baseline_logical_error_rate",
                value=0.0012,
                unit="ratio",
                direction="lower_is_better",
                notes="Baseline MWPM mock value.",
            ),
            BenchmarkMetric(
                name="decoder_candidate_logical_error_rate",
                value=comparison.logical_error_rate,
                unit="ratio",
                direction="lower_is_better",
                notes="Candidate decoder mock value.",
            ),
            BenchmarkMetric(
                name="syndrome_density_reduction",
                value=comparison.syndrome_density_reduction,
                unit="ratio",
                direction="higher_is_better",
                notes="Positive values indicate sparse syndrome representation.",
            ),
            BenchmarkMetric(
                name="estimated_latency_ms",
                value=comparison.estimated_latency_ms,
                unit="ms",
                direction="lower_is_better",
                notes="Estimated candidate decode latency.",
            ),
        ]
        report = BenchmarkReport(
            report_id=report_id,
            benchmark_type=f"qec_{code_type}_d{distance}",
            provider=provider,
            created_at=utcnow(),
            summary=BenchmarkSummary(
                headline=f"QEC benchmark for {code_type} d={distance}",
                key_findings=[
                    "Candidate decoder reduces latency in mock benchmark path.",
                    "Logical error rate trade-off requires follow-up investigation.",
                ],
            ),
            comparisons=[comparison],
            metrics=metrics,
            recommended_next_step=(
                "Run provider-backed benchmark with production syndrome traces "
                "and validate candidate decoder confidence interval."
            ),
            notes=[
                "Mock report generated for local development.",
                "Replace values with provider-derived benchmark telemetry when available.",
            ],
        )

        try:
            artifact_path = self._artifact_service.write_json(
                data=report.model_dump(),
                filename=f"{report_id}.json",
                sub_path="benchmarks",
            )
            artifact = BenchmarkArtifact(
                path=str(artifact_path),
                kind="benchmark_report",
                format="json",
                label="QEC benchmark report",
            )
            report = report.model_copy(
                update={
                    "artifact_paths": [artifact.path],
                    "artifacts": [artifact],
                }
            )
            logger.info("Benchmark artifact written: report_id=%s path=%s", report_id, artifact.path)
        except Exception:
            logger.exception("Failed to write benchmark artifact; continuing without artifact.")

        return report


_benchmark_service = BenchmarkService()


def get_benchmark_service() -> BenchmarkService:
    return _benchmark_service
