from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Settings."""

    postgres_dsn: str = Field("postgresql+asyncpg://app:123@localhost/social")


@lru_cache()
def get_settings():
    """Settings factory."""
    return Settings()
