import logging
import uuid
from functools import lru_cache

from api.endpoints.base import BaseService
from db.get_session import get_session
from fastapi import Depends
from models.authentication_models import RegistrationRequest
from schemas.schemas import UserData, Users
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
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
            )
            user_data = UserData(id=uuid.uuid4(), user_id=user.id)
            self.session.add_all((user, user_data))
            await self.session.commit()
        except IntegrityError as err:
            logger.info(err)
            await self.session.rollback()
            return False
        return True


@lru_cache()
def get_registration_service(
    engine: AsyncSession = Depends(get_session),
) -> RegistrationService:
    return RegistrationService(engine)
