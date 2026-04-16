"""Provider schemas."""

from enum import Enum

from pydantic import BaseModel, Field


class ProviderCapability(str, Enum):
    calibration_analysis = "calibration_analysis"
    calibration_workflows = "calibration_workflows"
    qec_decoding = "qec_decoding"
    qec_benchmarking = "qec_benchmarking"


class ProviderInfo(BaseModel):
    provider_id: str
    display_name: str
    version: str
    capabilities: list[ProviderCapability]
    description: str = ""
    is_available: bool = True


class ProviderListResponse(BaseModel):
    providers: list[ProviderInfo]
    total: int = Field(..., description="Total number of registered providers")
