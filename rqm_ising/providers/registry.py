"""Provider registry — runtime map of available provider implementations."""

from rqm_ising.config import get_settings
from rqm_ising.providers.base import BaseProvider


class ProviderRegistry:
    """
    Central registry for provider implementations.

    Providers register themselves at startup. Callers look up providers by
    their stable string ID. The registry is intentionally simple — it holds
    one instance per provider ID.
    """

    def __init__(self) -> None:
        self._providers: dict[str, BaseProvider] = {}

    def register(self, provider: BaseProvider) -> None:
        """Register a provider instance. Overwrites any existing entry with the same ID."""
        self._providers[provider.provider_id] = provider

    def get(self, provider_id: str) -> BaseProvider | None:
        """Return the provider with the given ID, or None if not registered."""
        return self._providers.get(provider_id)

    def get_or_raise(self, provider_id: str) -> BaseProvider:
        """Return the provider or raise ValueError if not found."""
        provider = self.get(provider_id)
        if provider is None:
            available = list(self._providers.keys())
            raise ValueError(
                f"Provider '{provider_id}' is not registered. "
                f"Available providers: {available}"
            )
        return provider

    def all(self) -> list[BaseProvider]:
        """Return all registered providers."""
        return list(self._providers.values())

    def ids(self) -> list[str]:
        """Return all registered provider IDs."""
        return list(self._providers.keys())


# Module-level singleton registry, populated at application startup
_registry = ProviderRegistry()


def get_registry() -> ProviderRegistry:
    """Return the global provider registry."""
    return _registry


def _bootstrap_default_providers() -> None:
    """Register built-in provider implementations."""
    from rqm_ising.providers.nvidia_ising import NvidiaIsingProvider

    settings = get_settings()
    if settings.enable_mock_providers:
        _registry.register(NvidiaIsingProvider())


# Bootstrap on module import so the registry is ready before the first request
_bootstrap_default_providers()
