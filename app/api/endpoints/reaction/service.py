import uuid
from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints.base import ServiceWithToken
from db.get_session import get_session
from models.reactions import Reactions
from schemas.schemas import UsersReactions
from utils.tokens import token_checkout


class ReactionsCrud(ServiceWithToken):
    """CRUD for reactions to post."""

    async def add_like(self, post_id: UUID) -> bool:
        """Add like for post."""
        return await self._add_like(str(post_id))

    async def _check_reaction(self, post_id: str) -> Optional[Reactions]:
        """Check the existence of a reaction."""
        stmt = select(UsersReactions.reaction).where(
            UsersReactions.post_id == post_id
            and UsersReactions.user_id == self.get_user_id()
        )
        request = await self.session.execute(stmt)
        response = request.scalar()
        if response is None:
            return
        elif response == Reactions.like:
            return Reactions.like
        else:
            return Reactions.dislike.value

    async def _add_like(self, post_id: str) -> bool:
        """Insert 'like' in database."""
        if await self._check_reaction(post_id) == (Reactions.dislike or None):
            like = UsersReactions(
                id=uuid.uuid4(),
                post_id=post_id,
                user_id=self.get_user_id(),
                reaction=Reactions.like,
            )
            self.session.add(like)
            await self.session.commit()

            return True
        return False

    async def del_like(self, post_id: UUID):
        """Delete like for post."""

    async def add_dislike(self, post_id: UUID):
        """Add dislike for post."""

    async def del_dislike(self, post_id: UUID):
        """Delete dislike for post."""

    async def del_reaction(self, post_id: UUID):
        """Delete reaction for post."""


def get_reaction_crud_service(
    token: str = Depends(token_checkout),
    session: AsyncSession = Depends(get_session),
) -> ReactionsCrud:
    return ReactionsCrud(session=session, token=token)
