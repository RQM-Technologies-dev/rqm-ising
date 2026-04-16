"""Benchmark/report schemas for Studio-facing workflow outputs."""

from datetime import datetime

from pydantic import BaseModel, Field


class BenchmarkArtifact(BaseModel):
    """File output associated with a benchmark or workflow report."""

    path: str
    kind: str = Field(default="report")
    format: str = Field(default="json")
    label: str = Field(default="Primary report output")


class BenchmarkMetric(BaseModel):
    """A normalized metric row that Studio can render in tables/charts."""

    name: str
    value: float
    unit: str = ""
    direction: str = Field(default="lower_is_better")
    notes: str = ""


class BenchmarkComparison(BaseModel):
    """Comparison between a baseline and candidate decoder/configuration."""

    decoder_baseline: str
    decoder_candidate: str
    logical_error_rate: float
    syndrome_density_reduction: float
    estimated_latency_ms: float
    confidence: float = Field(ge=0.0, le=1.0)
    notes: str = ""


class BenchmarkSummary(BaseModel):
    """Human-readable report summary block suitable for Studio cards."""

    headline: str
    key_findings: list[str] = Field(default_factory=list)


class BenchmarkReport(BaseModel):
    """Studio-friendly benchmark report schema."""

    report_id: str
    benchmark_type: str
    provider: str
    created_at: datetime
    summary: BenchmarkSummary
    comparisons: list[BenchmarkComparison] = Field(default_factory=list)
    metrics: list[BenchmarkMetric] = Field(default_factory=list)
    artifact_paths: list[str] = Field(default_factory=list)
    artifacts: list[BenchmarkArtifact] = Field(default_factory=list)
    recommended_next_step: str = ""
    notes: list[str] = Field(default_factory=list)
