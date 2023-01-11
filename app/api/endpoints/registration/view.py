from fastapi import APIRouter, Depends

from api.endpoints.registration.service import (
    RegistrationService,
    get_registration_service,
)
from models.authentication_models import (
    RegistrationResponse,
    RegistrationRequest,
    RegistrationStatus,
)

registration_router = APIRouter()


@registration_router.post(
    path="/",
    description="Reqeust for registration",
    response_model=RegistrationResponse,
)
async def registration(
    registration_request: RegistrationRequest,
    service: RegistrationService = Depends(get_registration_service),
):
    """Представление регистрации."""
    return RegistrationResponse(
        registration_status=RegistrationStatus.user_exists
    )
