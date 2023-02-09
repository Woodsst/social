from functools import lru_cache

from fastapi import Depends

from api.endpoints.login.repository import BaseLoginRepository, get_login_repo
from core.exceptions.jwt_exceptions import TokenValidityPeriodIsOver
from models.authentication_models import LoginRequest, LoginResponse
from utils.hashed_passwod import check_hashed_password
from utils.tokens import generate_jwt_tokens, update_access_token


class LoginService:
    """Service for a user login."""

    def __init__(self, repo: BaseLoginRepository):
        self.repo = repo

    async def login(self, user_data: LoginRequest) -> LoginResponse:
        """User login."""
        user_id, user_password = await self.repo.get_user_id_and_password(
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

    @staticmethod
    async def update_access(refresh_token: str):
        try:
            tokens = update_access_token(refresh_token)
            if tokens:
                access = tokens[0]
                refresh = tokens[1]
            else:
                return False
        except TokenValidityPeriodIsOver:
            return False
        return LoginResponse(
            access_token=access,
            refresh_token=refresh,
        )


@lru_cache()
def get_login_service(
    repo: BaseLoginRepository = Depends(get_login_repo),
) -> LoginService:
    return LoginService(repo)
