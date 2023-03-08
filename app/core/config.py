from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Settings."""

    postgres_dsn: str = Field("postgresql+asyncpg://app:123@localhost/social")
    jwt_algorithm: str = "HS256"
    jwt_access_secret: str = Field("super secret string for access token")
    jwt_refresh_secret: str = Field("super secret string for refresh token")
    jwt_access_lifetime_hour: int = Field(1)
    refresh_time = 14
    jwt_refresh_lifetime_day: int = Field(refresh_time)
    app_port: int = 8000
    app_host: str = "0.0.0.0"


@lru_cache()
def get_settings() -> Settings:
    """Settings factory."""
    return Settings()  # type: ignore
