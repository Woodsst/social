import logging
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import List

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints.base import Repository
from core.exceptions.user_exeptions import UserNotFound
from db.get_session import get_session
from models.user_page_models import UserDataInPage
from schemas.schemas import Users, Posts, UsersReactions

logger = logging.getLogger(__name__)


class BaseUserPageRepository(ABC):
    """Interface for user page repository."""

    @abstractmethod
    async def get_user_posts(
        self, user_id: str, page_size: int, page_number: int
    ) -> List[str]:
        """Request for getting user posts."""

    @abstractmethod
    async def get_user_data(self, user_id: str) -> UserDataInPage:
        """Request to the database to receive user data."""


class UserPageRepository(BaseUserPageRepository, Repository):
    """Work with Postgres repository for user page."""

    async def get_user_posts(
        self, user_id: str, page_size: int, page_number: int
    ) -> List[str]:
        """Request to the database to receive user posts."""
        stmt = (
            select(
                Posts.id.label("id"),
                Posts.post.label("content"),
                func.count(UsersReactions.r_like).label("like"),
                func.count(UsersReactions.r_dislike).label("dislike"),
                Posts.create_at,
            )
            .join(UsersReactions, isouter=True)
            .where(user_id == Posts.author_id)
            .group_by(
                Posts.id,
                Posts.create_at,
            )
            .order_by(Posts.create_at.desc())
            .limit(page_size)
            .offset(page_number * page_size)
        )
        request = await self.session.execute(stmt)
        return request.all()

    async def get_user_data(self, user_id: str) -> UserDataInPage:
        """Request to the database to receive user data."""
        stmt = select(Users.name, Users.sur_name, Users.date_of_birth).where(
            Users.id == user_id
        )
        reqeust = await self.session.execute(stmt)
        user_data = reqeust.first()
        if user_data is None:
            raise UserNotFound()

        return user_data


@lru_cache()
def get_user_page_repo(
    engine: AsyncSession = Depends(get_session),
) -> UserPageRepository:
    return UserPageRepository(engine)
