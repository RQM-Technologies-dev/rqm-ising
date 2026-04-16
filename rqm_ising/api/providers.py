"""Provider endpoints."""

from fastapi import APIRouter, Request

from rqm_ising.api.responses import error_response, success_response
from rqm_ising.providers.registry import get_registry
from rqm_ising.schemas.providers import ProviderListResponse

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("")
async def list_providers(request: Request):
    """Return all registered providers with status and integration metadata."""
    registry = get_registry()
    providers = [p.to_info().model_dump() for p in registry.all()]
    data = ProviderListResponse(providers=providers, total=len(providers)).model_dump()
    return success_response(request, data=data)


@router.get("/{provider_name}")
async def get_provider(provider_name: str, request: Request):
    """Return detailed provider health and integration status."""
    provider = get_registry().get(provider_name)
    if provider is None:
        return error_response(
            request,
            code="provider_not_found",
            message=f"Provider '{provider_name}' is not registered.",
            status_code=404,
        )
    return success_response(request, data=provider.to_detail().model_dump())
