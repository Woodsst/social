from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    """Parent for all services."""

    def __init__(self, session: AsyncSession):
        self.session = session
