"""
NVIDIA Ising QEC decoding adapter.

Translates between rqm-ising's provider-agnostic QEC schemas and the NVIDIA
Ising client interface. All NVIDIA-specific QEC field mappings belong here.
"""

import logging

from rqm_ising.providers.nvidia_ising.client import NvidiaIsingClient
from rqm_ising.schemas.qec import (
    QECBenchmarkRequest,
    QECBenchmarkRunResponse,
    QECDecodeRequest,
    QECDecodeSummary,
)
from rqm_ising.utils.ids import new_job_id

logger = logging.getLogger(__name__)


class NvidiaDecodingAdapter:
    """Adapts RQM QEC schemas to/from the NVIDIA Ising client."""

    def __init__(self, client: NvidiaIsingClient) -> None:
        self._client = client

    def decode(self, request: QECDecodeRequest) -> QECDecodeSummary:
        """
        Decode syndrome data via NVIDIA Ising and return a structured summary.

        In stub mode, returns realistic-looking mock data without calling any
        external service.
        """
        payload = {
            "run_id": request.run_id,
            "code_type": request.code_type,
            "distance": request.distance,
            "syndrome_data": request.syndrome_data,
            "decoder": request.decoder,
        }
        raw = self._client.submit_qec_decode(payload)
        logger.debug("nvidia qec decode raw response: %s", raw)

        warnings = (
            ["Running in stub mode — results are illustrative, not measured."]
            if not self._client.is_live
            else []
        )

        return QECDecodeSummary(
            run_id=request.run_id,
            provider="nvidia_ising",
            code_type=request.code_type,
            distance=request.distance,
            decoder=request.decoder,
            logical_error_rate=raw.get("logical_error_rate", 0.001),
            correction_count=raw.get("correction_count", 0),
            rounds_processed=raw.get("rounds_processed", len(request.syndrome_data)),
            decode_time_ms=raw.get("decode_time_ms", 0.0),
            warnings=warnings,
        )

    def benchmark(self, request: QECBenchmarkRequest) -> QECBenchmarkRunResponse:
        """Submit a QEC benchmark job via NVIDIA Ising."""
        payload = {
            "benchmark_id": request.benchmark_id,
            "code_type": request.code_type,
            "distance": request.distance,
            "decoders": request.decoders,
            "rounds": request.rounds,
        }
        raw = self._client.submit_qec_benchmark(payload)
        logger.debug("nvidia qec benchmark raw response: %s", raw)

        return QECBenchmarkRunResponse(
            job_id=new_job_id(),
            provider="nvidia_ising",
            benchmark_id=request.benchmark_id,
            status="pending",
        )
