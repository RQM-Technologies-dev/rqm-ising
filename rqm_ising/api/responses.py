"""Shared API response helpers with standardized envelope metadata."""

import time
from typing import Any

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from rqm_ising.schemas.common import make_error, make_success
from rqm_ising.utils.ids import new_request_id


def response_meta(request: Request) -> tuple[str, float]:
    """Return request_id and processing time in milliseconds."""
    request_id = getattr(request.state, "request_id", new_request_id())
    started = getattr(request.state, "request_started_at", None)
    processing_time_ms = (
        round((time.monotonic() - started) * 1000, 2)
        if isinstance(started, (int, float))
        else 0.0
    )
    return request_id, processing_time_ms


def success_response(request: Request, data: Any, status_code: int = 200) -> JSONResponse:
    """Create a success envelope response with metadata."""
    request_id, processing_time_ms = response_meta(request)
    return JSONResponse(
        status_code=status_code,
        content=make_success(
            data=jsonable_encoder(data),
            request_id=request_id,
            processing_time_ms=processing_time_ms,
        ),
    )


def error_response(
    request: Request,
    *,
    code: str,
    message: str,
    status_code: int,
) -> JSONResponse:
    """Create an error envelope response with metadata."""
    request_id, processing_time_ms = response_meta(request)
    return JSONResponse(
        status_code=status_code,
        content=make_error(
            code=code,
            message=message,
            request_id=request_id,
            processing_time_ms=processing_time_ms,
        ),
    )
