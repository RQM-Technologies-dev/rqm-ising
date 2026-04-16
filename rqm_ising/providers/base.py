"""Abstract base class for all quantum operation providers."""

from abc import ABC, abstractmethod

from rqm_ising.schemas.calibration import (
    CalibrationAnalysisResult,
    CalibrationAnalyzeRequest,
    CalibrationRunRequest,
    CalibrationRunResponse,
)
from rqm_ising.schemas.providers import ProviderCapability, ProviderInfo
from rqm_ising.schemas.qec import (
    QECBenchmarkRequest,
    QECBenchmarkRunResponse,
    QECDecodeRequest,
    QECDecodeSummary,
)


class BaseProvider(ABC):
    """
    All quantum operation providers must implement this interface.

    Each provider represents an external system (e.g., NVIDIA Ising) that can
    perform calibration analysis, calibration workflows, QEC decoding, or
    QEC benchmarking on behalf of the RQM integration layer.

    Implementations must be stateless with respect to job tracking — job
    lifecycle management is owned by JobService, not the provider.
    """

    # ── Identity ──────────────────────────────────────────────────────────────

    @property
    @abstractmethod
    def provider_id(self) -> str:
        """Stable, machine-readable provider identifier (e.g. 'nvidia_ising')."""
        ...

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable provider name."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Provider adapter version string."""
        ...

    @property
    @abstractmethod
    def capabilities(self) -> list[ProviderCapability]:
        """List of capabilities this provider supports."""
        ...

    @property
    def description(self) -> str:
        """Optional human-readable description of this provider."""
        return ""

    @property
    def is_available(self) -> bool:
        """Return True if the provider backend is currently reachable."""
        return True

    def to_info(self) -> ProviderInfo:
        """Serialize provider identity to ProviderInfo schema."""
        return ProviderInfo(
            provider_id=self.provider_id,
            display_name=self.display_name,
            version=self.version,
            capabilities=self.capabilities,
            description=self.description,
            is_available=self.is_available,
        )

    # ── Operations ────────────────────────────────────────────────────────────

    @abstractmethod
    def run_calibration_analysis(
        self, request: CalibrationAnalyzeRequest
    ) -> CalibrationAnalysisResult:
        """Run a calibration analysis and return a structured result."""
        ...

    @abstractmethod
    def run_calibration_workflow(
        self, request: CalibrationRunRequest
    ) -> CalibrationRunResponse:
        """Submit a calibration workflow and return a job handle."""
        ...

    @abstractmethod
    def run_qec_decoding(self, request: QECDecodeRequest) -> QECDecodeSummary:
        """Decode syndrome data and return a structured summary."""
        ...

    @abstractmethod
    def run_qec_benchmark(self, request: QECBenchmarkRequest) -> QECBenchmarkRunResponse:
        """Submit a QEC benchmark job and return a job handle."""
        ...
