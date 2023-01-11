from http import HTTPStatus

from api.endpoints.registration.service import (
    RegistrationService,
    get_registration_service,
)
from fastapi import APIRouter, Depends
from models.authentication_models import (
    RegistrationRequest,
    RegistrationResponse,
    RegistrationStatus,
)
from starlette.responses import JSONResponse

registration_router = APIRouter()


@registration_router.post(
    path="/",
    description="Reqeust for registration",
    response_model=RegistrationResponse,
    responses={HTTPStatus.CONFLICT.value: {"model": RegistrationResponse}},
)
async def registration(
    registration_request: RegistrationRequest,
    service: RegistrationService = Depends(get_registration_service),
):
    """Представление регистрации."""
    if await service.registration(registration_request):
        return RegistrationResponse(
            registration_status=RegistrationStatus.complete
        )
    else:
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content=RegistrationResponse(
                registration_status=RegistrationStatus.user_exists
            ).dict(),
        )
