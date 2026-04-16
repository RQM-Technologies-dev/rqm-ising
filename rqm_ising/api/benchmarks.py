"""Benchmark report endpoints."""

from fastapi import APIRouter, Request

from rqm_ising.api.responses import success_response
from rqm_ising.workflows.benchmark_workflow import generate_benchmark_report

router = APIRouter(prefix="/benchmarks", tags=["benchmarks"])


@router.get("/report")
async def benchmark_report(
    request: Request,
    code_type: str = "surface_code",
    distance: int = 5,
    provider: str = "nvidia_ising",
):
    """Return a structured benchmark report (mock in Phase 1)."""
    report = generate_benchmark_report(
        code_type=code_type,
        distance=distance,
        provider=provider,
    )
    return success_response(request, data=report.model_dump())
