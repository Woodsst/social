from sqlalchemy.ext.asyncio import AsyncSession

from utils.tokens import decode_access_token


class BaseService:
    """Parent for all services."""

    def __init__(self, session: AsyncSession):
        self.session = session


class ServiceWithToken:
    """Parent for all services with jwt."""

    def __init__(self, token: str):
        self.token = token

    def get_user_id(self):
        """Decode token to get user_id."""
        return decode_access_token(self.token).get("sub")
