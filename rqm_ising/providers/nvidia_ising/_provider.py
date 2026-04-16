"""
NVIDIA Ising provider implementation.

Wires the NvidiaIsingClient, calibration adapter, and decoding adapter
into the BaseProvider interface.
"""

import logging

from rqm_ising.providers.base import BaseProvider
from rqm_ising.providers.nvidia_ising.calibration_adapter import NvidiaCalibrationAdapter
from rqm_ising.providers.nvidia_ising.client import NvidiaIsingClient
from rqm_ising.providers.nvidia_ising.decoding_adapter import NvidiaDecodingAdapter
from rqm_ising.schemas.calibration import (
    CalibrationAnalysisResult,
    CalibrationAnalyzeRequest,
    CalibrationRunRequest,
    CalibrationRunResponse,
)
from rqm_ising.schemas.providers import ProviderCapability
from rqm_ising.schemas.qec import (
    QECBenchmarkRequest,
    QECBenchmarkRunResponse,
    QECDecodeRequest,
    QECDecodeSummary,
)

logger = logging.getLogger(__name__)


class NvidiaIsingProvider(BaseProvider):
    """
    Integration adapter for the NVIDIA Ising quantum operations backend.

    NVIDIA Ising is one provider in the rqm-ising ecosystem. This class
    implements the BaseProvider interface so it can be registered in the
    provider registry and used interchangeably with other providers.

    In stub/mock mode (no credentials configured), all operations return
    locally generated mock responses and are safe for development and CI.
    """

    def __init__(self) -> None:
        self._client = NvidiaIsingClient()
        self._cal_adapter = NvidiaCalibrationAdapter(self._client)
        self._dec_adapter = NvidiaDecodingAdapter(self._client)

    @property
    def provider_id(self) -> str:
        return "nvidia_ising"

    @property
    def display_name(self) -> str:
        return "NVIDIA Ising"

    @property
    def version(self) -> str:
        return "0.1.0-stub"

    @property
    def capabilities(self) -> list[ProviderCapability]:
        return [
            ProviderCapability.calibration_analysis,
            ProviderCapability.calibration_workflows,
            ProviderCapability.qec_decoding,
            ProviderCapability.qec_benchmarking,
        ]

    @property
    def description(self) -> str:
        return (
            "Integration adapter for NVIDIA Ising quantum operations. "
            "Provides calibration analysis, calibration workflows, QEC decoding, "
            "and QEC benchmarking via the NVIDIA Ising backend."
        )

    @property
    def is_available(self) -> bool:
        # In stub mode, the provider is always 'available' locally.
        # In live mode, availability depends on the backend being reachable.
        return True

    # ── BaseProvider interface ─────────────────────────────────────────────────

    def run_calibration_analysis(
        self, request: CalibrationAnalyzeRequest
    ) -> CalibrationAnalysisResult:
        return self._cal_adapter.analyze(request)

    def run_calibration_workflow(
        self, request: CalibrationRunRequest
    ) -> CalibrationRunResponse:
        return self._cal_adapter.run_workflow(request)

    def run_qec_decoding(self, request: QECDecodeRequest) -> QECDecodeSummary:
        return self._dec_adapter.decode(request)

    def run_qec_benchmark(self, request: QECBenchmarkRequest) -> QECBenchmarkRunResponse:
        return self._dec_adapter.benchmark(request)
