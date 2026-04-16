"""Shared test fixtures for rqm-ising."""

import pytest
from fastapi.testclient import TestClient

from rqm_ising.main import app


@pytest.fixture(scope="module")
def client():
    """Return a synchronous FastAPI test client."""
    with TestClient(app) as c:
        yield c
