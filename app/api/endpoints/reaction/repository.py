import uuid
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlalchemy import select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints.base import Repository
from db.get_session import get_session
from models.reactions import Reactions
from schemas.schemas import UsersReactions


class BaseReactionsRepository(ABC):
    """Interface from reactions repository."""

    @abstractmethod
    async def check_reaction(
        self, post_id: str, user_id: str
    ) -> Optional[Reactions]:
        """Check the existence of a reaction."""

    @abstractmethod
    async def add_reaction(
        self, reaction: Reactions, post_id: str, user_id: str
    ):
        """Insert new reaction from user."""

    @abstractmethod
    async def update_reaction(
        self, reaction: Reactions, post_id: str, user_id: str
    ):
        """Update user reaction."""

    @abstractmethod
    async def del_reaction(self, post_id: str, user_id: str):
        """Delete reaction from database."""


class ReactionsRepository(BaseReactionsRepository, Repository):
    async def check_reaction(
        self, post_id: str, user_id: str
    ) -> Optional[Reactions]:
        """Check the existence of a reaction."""
        stmt = select(UsersReactions.r_like, UsersReactions.r_dislike).where(
            UsersReactions.post_id == post_id,
            or_(
                UsersReactions.r_like == user_id,
                UsersReactions.r_dislike == user_id,
            ),
        )
        request = await self.session.execute(stmt)
        response = request.all()
        if len(response) == 0:
            return
        for i in response:
            if i._mapping.get("r_like"):
                return Reactions.like
            if i._mapping.get("r_dislike"):
                return Reactions.dislike

    async def add_reaction(
        self, reaction: Reactions, post_id: str, user_id: str
    ):
        """Insert new reaction from user."""
        if reaction == Reactions.like:
            user_reaction = UsersReactions(
                id=uuid.uuid4(),
                post_id=post_id,
                r_like=user_id,
            )
        else:
            user_reaction = UsersReactions(
                id=uuid.uuid4(),
                post_id=post_id,
                r_dislike=user_id,
            )
        self.session.add(user_reaction)
        await self.session.commit()

    async def update_reaction(
        self, reaction: Reactions, post_id: str, user_id: str
    ):
        """Update user reaction."""
        if reaction == Reactions.like:
            stmt = (
                update(UsersReactions)
                .where(
                    UsersReactions.post_id == post_id,
                    user_id == UsersReactions.r_dislike,
                )
                .values(r_like=user_id, r_dislike=None)
            )
        else:
            stmt = (
                update(UsersReactions)
                .where(
                    UsersReactions.post_id == post_id,
                    user_id == UsersReactions.r_like,
                )
                .values(r_dislike=user_id, r_like=None)
            )
        await self.session.execute(stmt)
        await self.session.commit()

    async def del_reaction(self, post_id: str, user_id: str):
        """Delete reaction from database."""
        stmt = delete(UsersReactions).where(
            UsersReactions.post_id == post_id,
            or_(
                user_id == UsersReactions.r_like,
                user_id == UsersReactions.r_dislike,
            ),
        )
        await self.session.execute(stmt)
        await self.session.commit()


@lru_cache()
def get_reactions_repo(
    engine: AsyncSession = Depends(get_session),
) -> ReactionsRepository:
    return ReactionsRepository(engine)
