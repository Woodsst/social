from functools import lru_cache

from fastapi import Depends

from api.endpoints.registration.repository import (
    BaseRegistrationRepository,
    get_registration_repo,
)
from models.authentication_models import RegistrationRequest


class RegistrationService:
    """Service for registration users."""

    def __init__(self, repo: BaseRegistrationRepository):
        self.repo = repo

    async def registration(self, registration_form: RegistrationRequest):
        """Registration new user."""
        return await self.repo.add_new_user(registration_form)


@lru_cache()
def get_registration_service(
    repo: BaseRegistrationRepository = Depends(get_registration_repo),
) -> RegistrationService:
    return RegistrationService(repo)
