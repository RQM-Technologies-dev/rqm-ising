"""FastAPI application entry point for rqm-ising."""

import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from rqm_ising import __version__
from rqm_ising.api import benchmarks, calibration, health, jobs, providers, qec
from rqm_ising.config import get_settings
from rqm_ising.logging import configure_logging
from rqm_ising.utils.ids import new_request_id

configure_logging()

settings = get_settings()

app = FastAPI(
    title="RQM Ising API",
    version=__version__,
    description=(
        "The quantum operations integration layer for calibration and QEC workflows "
        "in the RQM ecosystem. Connects external quantum hardware capabilities—initially "
        "NVIDIA Ising—into the broader RQM stack."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request-ID + timing middleware ────────────────────────────────────────────
@app.middleware("http")
async def request_metadata_middleware(request: Request, call_next):
    request_id = new_request_id()
    request.state.request_id = request_id
    start = time.monotonic()
    response = await call_next(request)
    elapsed_ms = round((time.monotonic() - start) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Processing-Time-Ms"] = str(elapsed_ms)
    return response


# ── Global error handler ──────────────────────────────────────────────────────
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", new_request_id())
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error": {
                "code": "internal_server_error",
                "message": "An unexpected error occurred.",
            },
            "meta": {
                "request_id": request_id,
                "processing_time_ms": None,
            },
        },
    )


# ── Health / version routes ───────────────────────────────────────────────────
app.include_router(health.router)


@app.get("/version", tags=["meta"])
async def version():
    return {"version": __version__}


# ── v1 API routes ─────────────────────────────────────────────────────────────
app.include_router(providers.router, prefix="/v1")
app.include_router(calibration.router, prefix="/v1")
app.include_router(qec.router, prefix="/v1")
app.include_router(jobs.router, prefix="/v1")
app.include_router(benchmarks.router, prefix="/v1")
