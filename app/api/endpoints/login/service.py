from functools import lru_cache

from api.endpoints.base import BaseService
from db.get_session import get_session
from fastapi import Depends
from models.authentication_models import (
    LoginRequest,
    LoginResponse,
)
from schemas.schemas import Users
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.hashed_passwod import check_hashed_password
from utils.tokens import generate_jwt_tokens


class LoginService(BaseService):
    """Service for a user login."""

    async def login(self, user_data: LoginRequest) -> LoginResponse:
        """User login."""
        user_id, user_password = await self._get_user_id_and_password(
            user_data.login
        )
        if user_id is None:
            return

        if check_hashed_password(user_data.password, user_password):
            access, refresh = generate_jwt_tokens(str(user_id))
            return LoginResponse(
                access_token=access,
                refresh_token=refresh,
            )

    async def _get_user_id_and_password(self, login: str) -> str:
        """Request in db for get user id."""
        stmt = select(Users.id, Users.password).where(Users.login == login)
        request = await self.session.execute(stmt)
        response = request.first()
        if response is None:
            return None, None
        return response


@lru_cache()
def get_login_service(
    engine: AsyncSession = Depends(get_session),
) -> LoginService:
    return LoginService(engine)
