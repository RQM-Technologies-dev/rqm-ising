"""FastAPI application entry point for rqm-ising."""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from rqm_ising import __version__
from rqm_ising.api import benchmarks, calibration, health, jobs, providers, qec
from rqm_ising.api.responses import error_response, success_response
from rqm_ising.config import get_settings
from rqm_ising.logging import configure_logging, get_logger
from rqm_ising.services.artifact_service import get_artifact_service
from rqm_ising.services.job_service import get_job_service
from rqm_ising.utils.ids import new_request_id

configure_logging()
logger = get_logger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize local directories and reload persisted jobs on startup."""
    artifact_service = get_artifact_service()
    artifact_service.ensure_dir()
    artifact_service.ensure_dir("jobs")
    job_service = get_job_service()
    job_service.load_persisted_jobs()
    yield

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
    lifespan=lifespan,
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
    request.state.request_started_at = start
    logger.debug(
        "Request started: request_id=%s method=%s path=%s",
        request_id,
        request.method,
        request.url.path,
    )
    response = await call_next(request)
    elapsed_ms = round((time.monotonic() - start) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Processing-Time-Ms"] = str(elapsed_ms)
    logger.debug(
        "Request completed: request_id=%s method=%s path=%s status=%s elapsed_ms=%s",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


# ── Global error handler ──────────────────────────────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first = exc.errors()[0] if exc.errors() else {}
    detail = first.get("msg", "Invalid request payload.")
    return error_response(
        request,
        code="validation_error",
        message=f"Request validation failed: {detail}",
        status_code=422,
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = str(exc.detail) if exc.detail else "Request failed."
    return error_response(
        request,
        code="http_error",
        message=detail,
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled exception: request_id=%s error=%s",
        getattr(request.state, "request_id", "missing"),
        exc,
    )
    del exc
    return error_response(
        request,
        code="internal_server_error",
        message="An unexpected error occurred.",
        status_code=500,
    )


# ── Health / version routes ───────────────────────────────────────────────────
app.include_router(health.router)


@app.get("/version", tags=["meta"])
async def version(request: Request):
    return success_response(request, data={"version": __version__})


# ── v1 API routes ─────────────────────────────────────────────────────────────
app.include_router(providers.router, prefix="/v1")
app.include_router(calibration.router, prefix="/v1")
app.include_router(qec.router, prefix="/v1")
app.include_router(jobs.router, prefix="/v1")
app.include_router(benchmarks.router, prefix="/v1")
