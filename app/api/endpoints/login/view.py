from http import HTTPStatus
from typing import Union

from fastapi import APIRouter, Depends, Header
from starlette.responses import JSONResponse

from api.endpoints.login.service import LoginService, get_login_service
from models.authentication_models import (
    LoginRequest,
    LoginResponse,
    LoginWrong,
    Tokens,
    WrongToken,
)

login_router = APIRouter()


@login_router.post(
    path="/",
    description="Reqeust for login",
    response_model=LoginResponse,
    responses={HTTPStatus.CONFLICT.value: {"model": LoginWrong}},
)
async def login(
    login_request: LoginRequest,
    service: LoginService = Depends(get_login_service),
) -> Union[JSONResponse, LoginResponse]:
    """Login view."""
    tokens = await service.login(login_request)
    if tokens:
        return tokens
    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content=LoginWrong().dict(),
    )


@login_router.get(
    path="/update",
    description="Update access token",
    response_model=Tokens,
    responses={HTTPStatus.CONFLICT.value: {"model": WrongToken}},
)
async def update_access_token(
    refresh_token: str = Header(),
    service: LoginService = Depends(get_login_service),
) -> Union[JSONResponse, LoginResponse]:
    """Update access token by refresh token."""
    tokens = await service.update_access(refresh_token)
    if tokens:
        return tokens
    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content=WrongToken().dict(),
    )
