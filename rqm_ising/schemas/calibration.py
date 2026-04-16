"""Calibration task schemas."""

from pydantic import BaseModel, Field


class CalibrationAnalyzeRequest(BaseModel):
    """Request metadata for a calibration analysis run."""

    experiment_id: str = Field(..., description="Caller-assigned experiment identifier")
    qubit_count: int = Field(..., ge=1, description="Number of qubits in the experiment")
    coupling_map: list[list[int]] = Field(
        default_factory=list,
        description="List of [control, target] qubit pairs describing the device topology",
    )
    gate_set: list[str] = Field(
        default_factory=list,
        description="Gate names available on the device",
    )
    noise_metadata: dict = Field(
        default_factory=dict,
        description="Provider-agnostic noise characterisation metadata",
    )
    provider: str = Field(default="nvidia_ising", description="Target provider identifier")


class CalibrationAnalysisResult(BaseModel):
    """Structured output of a calibration analysis."""

    experiment_id: str
    provider: str
    qubit_count: int
    recommended_gate_fidelities: dict[str, float]
    t1_estimates_us: dict[str, float]
    t2_estimates_us: dict[str, float]
    noise_model_summary: str
    analysis_warnings: list[str] = Field(default_factory=list)


class CalibrationRunRequest(BaseModel):
    """Request to submit a full calibration workflow job."""

    experiment_id: str
    qubit_count: int
    coupling_map: list[list[int]] = Field(default_factory=list)
    gate_set: list[str] = Field(default_factory=list)
    workflow_params: dict = Field(
        default_factory=dict,
        description="Provider-specific workflow parameters passed through without interpretation",
    )
    provider: str = Field(default="nvidia_ising")


class CalibrationRunResponse(BaseModel):
    job_id: str
    provider: str
    experiment_id: str
    status: str
    artifact_paths: list[str] = Field(default_factory=list)
    result_summary: dict = Field(default_factory=dict)
