from functools import lru_cache
from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints.base import BaseService
from db.get_session import get_session
from models.authentication_models import LoginRequest
from sqlalchemy.future import select
from schemas.schemas import Users
from utils.hashed_passwod import check_hashed_password


class LoginService(BaseService):
    """Service for a user login."""

    async def check_password(self, user_data: LoginRequest) -> bool:
        """Check password."""
        hashed_password = await self._get_password(user_data.login)

        if hashed_password:
            return check_hashed_password(user_data.password, hashed_password)

    async def _get_password(self, login: str) -> Optional[str]:
        """Request in db for get password."""
        stmt = select(Users.password).where(Users.login == login)
        request = await self.session.execute(stmt)
        password = request.first()

        if password is None:
            return

        return password[0]

    async def _generate_jwt_tokens(self, user_id: UUID):
        pass


@lru_cache()
def get_login_service(
    engine: AsyncSession = Depends(get_session),
) -> LoginService:
    return LoginService(engine)
