"""Provider schemas."""

from enum import StrEnum

from pydantic import BaseModel, Field


class ProviderCapability(StrEnum):
    calibration_analysis = "calibration_analysis"
    calibration_workflows = "calibration_workflows"
    qec_decoding = "qec_decoding"
    qec_benchmarking = "qec_benchmarking"


class ProviderIntegrationMode(StrEnum):
    mock = "mock"
    configured = "configured"
    unavailable = "unavailable"


class ProviderStatus(StrEnum):
    available = "available"
    unavailable = "unavailable"


class ProviderInfo(BaseModel):
    name: str
    display_name: str
    capabilities: list[ProviderCapability]
    status: ProviderStatus
    integration_mode: ProviderIntegrationMode
    summary: str


class ProviderDetailResponse(BaseModel):
    name: str
    display_name: str
    version: str
    capabilities: list[ProviderCapability]
    status: ProviderStatus
    availability: bool
    credentials_configured: bool
    externally_connected: bool
    mock_only: bool
    integration_mode: ProviderIntegrationMode
    summary: str
    description: str = ""


class ProviderListResponse(BaseModel):
    providers: list[ProviderInfo]
    total: int = Field(..., description="Total number of registered providers")
