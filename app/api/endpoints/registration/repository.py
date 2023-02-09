import logging
import uuid
from abc import ABC, abstractmethod
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints.base import Repository
from db.get_session import get_session
from models.authentication_models import RegistrationRequest
from schemas.schemas import Users
from utils.hashed_passwod import hash_password

logger = logging.getLogger(__name__)


class BaseRegistrationRepository(ABC):
    """Interface for registration repository."""

    @abstractmethod
    async def add_new_user(
        self, registration_form: RegistrationRequest
    ) -> bool:
        """Add new user in database."""


class RegistrationRepository(BaseRegistrationRepository, Repository):
    """Postgres repository."""

    async def add_new_user(
        self, registration_form: RegistrationRequest
    ) -> bool:
        """Query for add new user in database."""
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
def get_registration_repo(
    engine: AsyncSession = Depends(get_session),
) -> RegistrationRepository:
    return RegistrationRepository(engine)
