from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

engine: Optional[AsyncEngine] = None
sql_session: Optional[AsyncSession] = None


async def get_session() -> AsyncSession:
    async with sql_session() as session:
        yield session
