"""ID generation utilities."""

import uuid


def new_id() -> str:
    """Generate a new random UUID string."""
    return str(uuid.uuid4())


def new_request_id() -> str:
    """Generate a request-scoped trace ID with a readable prefix."""
    return f"req_{uuid.uuid4().hex[:12]}"


def new_job_id() -> str:
    """Generate a job ID with a readable prefix."""
    return f"job_{uuid.uuid4().hex[:16]}"


def new_artifact_id() -> str:
    """Generate an artifact ID with a readable prefix."""
    return f"art_{uuid.uuid4().hex[:16]}"
