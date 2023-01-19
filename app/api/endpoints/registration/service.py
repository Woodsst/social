import logging
import uuid
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints.base import BaseService
from db.get_session import get_session
from models.authentication_models import RegistrationRequest
from schemas.schemas import Users
from utils.hashed_passwod import hash_password

logger = logging.getLogger(__name__)


class RegistrationService(BaseService):
    """Service for registration users."""

    async def registration(
        self, registration_form: RegistrationRequest
    ) -> bool:
        try:
            user = Users(
                id=uuid.uuid4(),
                login=registration_form.login,
                password=hash_password(registration_form.password),
                email=registration_form.email,
                name=registration_form.name,
            )
            self.session.add(user)
            await self.session.commit()
        except IntegrityError as err:
            logger.info(err)
            await self.session.rollback()
            return False
        return True


@lru_cache()
def get_registration_service(
    session: AsyncSession = Depends(get_session),
) -> RegistrationService:
    return RegistrationService(session)
