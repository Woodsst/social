from fastapi import APIRouter, Depends

from api.endpoints.login.service import (
    LoginService,
    get_login_service,
)
from models.authentication_models import (
    LoginResponse,
    LoginRequest,
    LoginStatus,
)

login_router = APIRouter()


@login_router.post(
    path="/",
    description="Reqeust for registration",
    response_model=LoginResponse,
)
async def registration(
    registration_request: LoginRequest,
    service: LoginService = Depends(get_login_service),
):
    """Представление аутентификации."""
    return LoginResponse(registration_status=LoginStatus.wrong_password)
