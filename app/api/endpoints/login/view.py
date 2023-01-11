from http import HTTPStatus

from api.endpoints.login.service import LoginService, get_login_service
from fastapi import APIRouter, Depends
from models.authentication_models import (
    LoginRequest,
    LoginResponse,
    LoginWrong,
)
from starlette.responses import JSONResponse

login_router = APIRouter()


@login_router.get(
    path="/",
    description="Reqeust for login",
    response_model=LoginResponse,
    responses={HTTPStatus.CONFLICT.value: {"model": LoginWrong}},
)
async def registration(
    login_request: LoginRequest,
    service: LoginService = Depends(get_login_service),
):
    """Представление аутентификации."""
    tokens = await service.login(login_request)
    if tokens:
        return tokens
    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content=LoginWrong().dict(),
    )
