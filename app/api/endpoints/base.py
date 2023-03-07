from typing import Dict, Any

from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession

from utils.tokens import decode_access_token


class Repository:
    """Parent for all repository."""

    def __init__(self, session: AsyncSession):
        self.session = session


class ServiceWithToken:
    """Parent for all services with jwt."""

    def __init__(self, token: str):
        self.token = token

    def get_user_id(self) -> Any:
        """Decode token to get user_id."""
        return decode_access_token(self.token).get("sub")


class Paginator:
    """Paginator for views."""

    def __init__(
        self,
        page_size: int = Query(
            ge=0,
            le=50,
            default=10,
            description="Items amount on page",
        ),
        page_number: int = Query(
            default=0,
            ge=0,
            description="Page number for pagination",
        ),
    ):
        self.page_size = page_size
        self.page_number = page_number
