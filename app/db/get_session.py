from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

engine: Optional[AsyncEngine] = None
sql_session: Optional[AsyncSession] = None


def get_session():
    return sql_session
