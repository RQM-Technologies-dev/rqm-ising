"""Common response envelope schemas shared across all endpoints."""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseMeta(BaseModel):
    request_id: str = Field(..., description="Unique identifier for this request")
    processing_time_ms: float | None = Field(
        None, description="Server-side processing time in milliseconds"
    )


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success envelope."""

    status: str = "success"
    data: T
    meta: ResponseMeta


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error description")


class ErrorResponse(BaseModel):
    """Standard error envelope."""

    status: str = "error"
    error: ErrorDetail
    meta: ResponseMeta


def make_success(data: Any, request_id: str, processing_time_ms: float | None = None) -> dict:
    """Build a success envelope dict."""
    return {
        "status": "success",
        "data": data,
        "meta": {
            "request_id": request_id,
            "processing_time_ms": processing_time_ms,
        },
    }


def make_error(
    code: str,
    message: str,
    request_id: str,
    processing_time_ms: float | None = None,
) -> dict:
    """Build an error envelope dict."""
    return {
        "status": "error",
        "error": {"code": code, "message": message},
        "meta": {
            "request_id": request_id,
            "processing_time_ms": processing_time_ms,
        },
    }
