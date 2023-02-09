import uuid
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlalchemy import select, update, delete
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
        stmt = select(UsersReactions.reaction).where(
            UsersReactions.post_id == post_id
            and UsersReactions.user_id == user_id
        )
        request = await self.session.execute(stmt)
        response = request.scalar()
        if response is None:
            return
        elif response == Reactions.like:
            return Reactions.like
        else:
            return Reactions.dislike.value

    async def add_reaction(
        self, reaction: Reactions, post_id: str, user_id: str
    ):
        """Insert new reaction from user."""
        user_reaction = UsersReactions(
            id=uuid.uuid4(),
            post_id=post_id,
            user_id=user_id,
            reaction=reaction,
        )
        self.session.add(user_reaction)
        await self.session.commit()

    async def update_reaction(
        self, reaction: Reactions, post_id: str, user_id: str
    ):
        """Update user reaction."""
        stmt = (
            update(UsersReactions)
            .where(
                UsersReactions.post_id == post_id
                and user_id == UsersReactions.user_id
            )
            .values(reaction=reaction)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def del_reaction(self, post_id: str, user_id: str):
        """Delete reaction from database."""
        stmt = delete(UsersReactions).where(
            UsersReactions.post_id == post_id
            and user_id == UsersReactions.user_id
        )
        await self.session.execute(stmt)
        await self.session.commit()


@lru_cache()
def get_reactions_repo(
    engine: AsyncSession = Depends(get_session),
) -> ReactionsRepository:
    return ReactionsRepository(engine)
