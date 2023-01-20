from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    """Parent for all services."""

    def __init__(self, session: AsyncSession):
        self.session = session


class ServiceWithToken(BaseService):
    """Parent for all services with jwt."""

    def __init__(self, session: AsyncSession, token: str):
        super().__init__(session=session)
        self.token = token
