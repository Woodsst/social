from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Settings."""

    url: str = Field("http://localhost:8000/api/")

    postgres_test_dsn: str = Field("postgresql://app:123@localhost/social")
    jwt_algorithm: str = "HS256"
    jwt_access_secret: str = Field("super secret string for access token")
    jwt_refresh_secret: str = Field("super secret string for refresh token")
    jwt_access_lifetime_hour: int = Field(1)
    refresh_time = 14
    jwt_refresh_lifetime_day: int = Field(refresh_time)


@lru_cache()
def get_settings() -> Settings:
    """Settings factory."""
    return Settings()  # type: ignore
