"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RQM_ISING_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    env: str = "development"
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000

    # Artifact storage
    artifact_dir: str = "./artifacts"

    # CORS — comma-separated list of allowed origins
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


class NvidiaIsingSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="NVIDIA_ISING_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    base_url: str = ""
    api_key: str = ""
    timeout_seconds: int = 30

    @property
    def is_configured(self) -> bool:
        """Return True when a live NVIDIA Ising endpoint is configured."""
        return bool(self.base_url and self.api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_nvidia_settings() -> NvidiaIsingSettings:
    return NvidiaIsingSettings()
