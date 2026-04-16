"""
NVIDIA Ising–specific Pydantic models.

These models represent the internal request/response shapes for the NVIDIA
Ising API. They are intentionally separate from the shared rqm_ising schemas
so that NVIDIA-specific field naming does not bleed into the public API contract.
"""

from pydantic import BaseModel, Field


class NvidiaCalibrationRequest(BaseModel):
    experiment_id: str
    qubit_count: int
    coupling_map: list[list[int]] = Field(default_factory=list)
    gate_set: list[str] = Field(default_factory=list)
    noise_metadata: dict = Field(default_factory=dict)


class NvidiaCalibrationAnalysisResponse(BaseModel):
    status: str
    analysis_id: str
    source: str


class NvidiaQECDecodeRequest(BaseModel):
    run_id: str
    code_type: str
    distance: int
    syndrome_data: list[list[int]]
    decoder: str = "mwpm"


class NvidiaQECDecodeResponse(BaseModel):
    status: str
    logical_error_rate: float
    correction_count: int
    rounds_processed: int
    decode_time_ms: float
    source: str
