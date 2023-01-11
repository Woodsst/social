from http import HTTPStatus

from api.endpoints.login.service import LoginService, get_login_service
from fastapi import APIRouter, Depends
from models.authentication_models import (
    LoginRequest,
    LoginResponse,
    LoginStatus,
)

login_router = APIRouter()


@login_router.post(
    path="/",
    description="Reqeust for login",
    response_model=LoginResponse,
    responses={HTTPStatus.CONFLICT.value: {"model": LoginResponse}},
)
async def registration(
    login_request: LoginRequest,
    service: LoginService = Depends(get_login_service),
):
    """Представление аутентификации."""
    if await service.check_password(login_request):
        pass
    return LoginResponse(registration_status=LoginStatus.wrong_password)
