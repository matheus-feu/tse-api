from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "TSE Data API"
    APP_VERSION: str = "1.0"
    DEBUG: bool = False
    LOCALIZATION_API_URL: str = "https://apps.tre-sp.jus.br/api-gateway/zonaEleitoral/1.0"
    DATABASE_URL: str | None = None
    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """Get application settings with caching to avoid reloading."""
    return Settings()


settings = get_settings()
