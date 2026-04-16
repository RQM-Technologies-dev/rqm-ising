"""Abstract base class for all quantum operation providers."""

from abc import ABC, abstractmethod

from rqm_ising.schemas.calibration import (
    CalibrationAnalysisResult,
    CalibrationAnalyzeRequest,
    CalibrationRunRequest,
    CalibrationRunResponse,
)
from rqm_ising.schemas.providers import (
    ProviderCapability,
    ProviderDetailResponse,
    ProviderInfo,
    ProviderIntegrationMode,
    ProviderStatus,
)
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

    @property
    def credentials_configured(self) -> bool:
        """Return True if provider credentials/config are present."""
        return False

    @property
    def externally_connected(self) -> bool:
        """Return True if requests are sent to an external backend."""
        return False

    @property
    def mock_only(self) -> bool:
        """Return True if provider is currently mock-only."""
        return not self.externally_connected

    @property
    def status(self) -> ProviderStatus:
        return ProviderStatus.available if self.is_available else ProviderStatus.unavailable

    @property
    def integration_mode(self) -> ProviderIntegrationMode:
        if not self.is_available:
            return ProviderIntegrationMode.unavailable
        if self.externally_connected and self.credentials_configured:
            return ProviderIntegrationMode.configured
        return ProviderIntegrationMode.mock

    @property
    def summary(self) -> str:
        if self.integration_mode == ProviderIntegrationMode.configured:
            return "Provider configured and available for external execution."
        if self.integration_mode == ProviderIntegrationMode.mock:
            return "Provider running in mock mode for local development."
        return "Provider unavailable."

    def to_info(self) -> ProviderInfo:
        """Serialize provider identity to ProviderInfo schema."""
        return ProviderInfo(
            name=self.provider_id,
            display_name=self.display_name,
            capabilities=self.capabilities,
            status=self.status,
            integration_mode=self.integration_mode,
            summary=self.summary,
        )

    def to_detail(self) -> ProviderDetailResponse:
        """Serialize provider detail for status endpoint."""
        return ProviderDetailResponse(
            name=self.provider_id,
            display_name=self.display_name,
            version=self.version,
            capabilities=self.capabilities,
            status=self.status,
            availability=self.is_available,
            credentials_configured=self.credentials_configured,
            externally_connected=self.externally_connected,
            mock_only=self.mock_only,
            integration_mode=self.integration_mode,
            summary=self.summary,
            description=self.description,
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
