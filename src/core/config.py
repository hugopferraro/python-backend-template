from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Basic src info
    APP_NAME: str = "FastAPI Template"
    APP_ENV: str = "dev"  # dev | staging | prod

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    # Data Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    # API Security
    ALLOWED_ORIGINS: list[str] = []

    # Logging
    LOG_LEVEL: str = "INFO"  # DEBUG | INFO | WARNING | ERROR | CRITICAL
    LOG_SQL_QUERIES: bool = False  # Set to False to disable SQL query logging


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Cached so we don't recreate Settings on every import.
    """
    return Settings()