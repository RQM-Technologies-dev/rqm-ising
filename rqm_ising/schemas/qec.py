"""QEC (Quantum Error Correction) schemas."""

from pydantic import BaseModel, Field


class QECDecodeRequest(BaseModel):
    """Request to decode syndrome data."""

    run_id: str = Field(..., description="Caller-assigned run identifier")
    code_type: str = Field(..., description="Error-correcting code type, e.g. 'surface_code'")
    distance: int = Field(..., ge=2, description="Code distance")
    syndrome_data: list[list[int]] = Field(
        ...,
        description="Syndrome measurement rounds as a 2-D binary array [rounds × stabilizers]",
    )
    decoder: str = Field(default="mwpm", description="Decoder algorithm identifier")
    provider: str = Field(default="nvidia_ising")


class QECDecodeSummary(BaseModel):
    """Structured output of a QEC decode operation."""

    run_id: str
    provider: str
    code_type: str
    distance: int
    decoder: str
    logical_error_rate: float
    correction_count: int
    rounds_processed: int
    decode_time_ms: float
    warnings: list[str] = Field(default_factory=list)


class QECBenchmarkRequest(BaseModel):
    """Request to submit a QEC benchmark job comparing decoder approaches."""

    benchmark_id: str = Field(..., description="Caller-assigned benchmark identifier")
    code_type: str
    distance: int = Field(..., ge=2)
    decoders: list[str] = Field(..., min_length=1, description="List of decoder identifiers to compare")
    rounds: int = Field(default=1000, ge=1)
    provider: str = Field(default="nvidia_ising")


class QECBenchmarkRunResponse(BaseModel):
    job_id: str
    provider: str
    benchmark_id: str
    status: str
