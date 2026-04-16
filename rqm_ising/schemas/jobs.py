"""Job schemas."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class JobType(str, Enum):
    calibration_analysis = "calibration_analysis"
    calibration_workflow = "calibration_workflow"
    qec_decode = "qec_decode"
    qec_benchmark = "qec_benchmark"
    benchmark_report = "benchmark_report"


class Job(BaseModel):
    job_id: str
    type: JobType
    status: JobStatus
    provider: str
    input_summary: dict = Field(default_factory=dict)
    artifact_paths: list[str] = Field(default_factory=list)
    result_summary: dict | None = None
    created_at: datetime
    updated_at: datetime


class JobListResponse(BaseModel):
    jobs: list[Job]
    total: int
