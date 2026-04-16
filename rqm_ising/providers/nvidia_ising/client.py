"""
NVIDIA Ising HTTP client stub.

This module is the integration boundary for the NVIDIA Ising backend.
In production, replace the stub methods with real HTTP calls to the
NVIDIA Ising API using the configured base URL and API key.

Do NOT embed NVIDIA-specific logic in shared services or schemas.
All NVIDIA-specific request/response translation lives in this package.
"""

import logging

from rqm_ising.config import get_nvidia_settings

logger = logging.getLogger(__name__)


class NvidiaIsingClient:
    """
    Thin HTTP client for the NVIDIA Ising backend.

    When `NvidiaIsingSettings.is_configured` is False (the default for local
    development), all methods return stub responses so the service is fully
    runnable without external credentials.
    """

    def __init__(self) -> None:
        self._settings = get_nvidia_settings()
        if self._settings.is_configured:
            logger.info("NvidiaIsingClient: live mode (base_url=%s)", self._settings.base_url)
        else:
            logger.info("NvidiaIsingClient: stub/mock mode (no credentials configured)")

    @property
    def is_live(self) -> bool:
        return self._settings.is_configured

    # ── Calibration ───────────────────────────────────────────────────────────

    def submit_calibration_analysis(self, payload: dict) -> dict:
        """
        Submit a calibration analysis request to NVIDIA Ising.

        Integration point: replace stub with a POST to
        {base_url}/calibration/analyze with bearer token from api_key.
        """
        if self.is_live:
            raise NotImplementedError(
                "Live NVIDIA Ising calibration analysis is not yet implemented. "
                "Implement HTTP call here."
            )
        # Stub response — safe for local development and CI
        return {
            "status": "ok",
            "analysis_id": payload.get("experiment_id", "stub-exp"),
            "source": "nvidia_ising_stub",
        }

    def submit_calibration_workflow(self, payload: dict) -> dict:
        """
        Submit a calibration workflow job to NVIDIA Ising.

        Integration point: replace stub with a POST to
        {base_url}/calibration/run with bearer token from api_key.
        """
        if self.is_live:
            raise NotImplementedError(
                "Live NVIDIA Ising calibration workflow is not yet implemented."
            )
        return {
            "status": "accepted",
            "remote_job_id": "nvidia-stub-job-cal-001",
            "source": "nvidia_ising_stub",
        }

    # ── QEC ───────────────────────────────────────────────────────────────────

    def submit_qec_decode(self, payload: dict) -> dict:
        """
        Submit syndrome data for QEC decoding to NVIDIA Ising.

        Integration point: replace stub with a POST to
        {base_url}/qec/decode with bearer token from api_key.
        """
        if self.is_live:
            raise NotImplementedError(
                "Live NVIDIA Ising QEC decoding is not yet implemented."
            )
        syndrome_data = payload.get("syndrome_data", [])
        rounds = len(syndrome_data)
        return {
            "status": "ok",
            "logical_error_rate": 0.0012,
            "correction_count": max(1, rounds // 10),
            "rounds_processed": rounds,
            "decode_time_ms": 4.2,
            "source": "nvidia_ising_stub",
        }

    def submit_qec_benchmark(self, payload: dict) -> dict:
        """
        Submit a QEC benchmark job to NVIDIA Ising.

        Integration point: replace stub with a POST to
        {base_url}/qec/benchmark with bearer token from api_key.
        """
        if self.is_live:
            raise NotImplementedError(
                "Live NVIDIA Ising QEC benchmark is not yet implemented."
            )
        return {
            "status": "accepted",
            "remote_job_id": "nvidia-stub-job-qec-001",
            "source": "nvidia_ising_stub",
        }
