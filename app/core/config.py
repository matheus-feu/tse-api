from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "TSE Data API"
    APP_VERSION: str = "1.0"
    DEBUG: bool = False

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "tse"
    DB_USER: str = "root"
    DB_PASSWORD: str = "root"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """Get application settings with caching to avoid reloading."""
    return Settings()


settings = get_settings()
