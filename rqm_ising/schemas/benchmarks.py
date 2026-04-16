"""Benchmark report schemas."""

from pydantic import BaseModel, Field


class DecoderBenchmarkEntry(BaseModel):
    decoder: str
    logical_error_rate: float
    avg_decode_time_ms: float
    rounds_tested: int


class BenchmarkReport(BaseModel):
    """Structured benchmark report returned by /v1/benchmarks/report."""

    report_id: str
    code_type: str
    distance: int
    provider: str
    entries: list[DecoderBenchmarkEntry] = Field(default_factory=list)
    summary: str = ""
    artifact_path: str | None = None
