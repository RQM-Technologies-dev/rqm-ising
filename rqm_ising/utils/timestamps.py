"""Timestamp utilities for rqm-ising."""

from datetime import UTC, datetime


def utcnow() -> datetime:
    """Return the current UTC datetime (timezone-aware)."""
    return datetime.now(UTC)


def utcnow_iso() -> str:
    """Return the current UTC datetime as an ISO 8601 string."""
    return utcnow().isoformat()
