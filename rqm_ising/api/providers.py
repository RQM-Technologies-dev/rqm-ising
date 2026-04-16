"""Provider endpoints."""

from fastapi import APIRouter, Request

from rqm_ising.providers.registry import get_registry
from rqm_ising.schemas.common import make_success
from rqm_ising.schemas.providers import ProviderListResponse
from rqm_ising.utils.ids import new_request_id

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("")
async def list_providers(request: Request):
    """Return all registered providers and their capabilities."""
    request_id = getattr(request.state, "request_id", new_request_id())
    registry = get_registry()
    providers = [p.to_info().model_dump() for p in registry.all()]
    data = ProviderListResponse(providers=providers, total=len(providers)).model_dump()
    return make_success(data=data, request_id=request_id)
