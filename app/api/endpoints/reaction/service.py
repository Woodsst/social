import uuid
from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints.base import ServiceWithToken
from db.get_session import get_session
from models.reactions import Reactions
from schemas.schemas import UsersReactions
from utils.tokens import token_checkout


class ReactionsCrud(ServiceWithToken):
    """CRUD for reactions to post."""

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

    async def add_reaction(self, reaction: Reactions, post_id: str):
        """Add reaction from user."""
        existing_reaction = await self._check_reaction(post_id)
        if existing_reaction is None:
            await self._add_reaction(reaction, post_id)
        elif existing_reaction != reaction:
            await self._update_reaction(reaction, post_id)
            return True
        return False

    async def _add_reaction(self, reaction: Reactions, post_id: str):
        """Insert new reaction from user."""
        user_reaction = UsersReactions(
            id=uuid.uuid4(),
            post_id=post_id,
            user_id=self.get_user_id(),
            reaction=reaction,
        )
        self.session.add(user_reaction)
        await self.session.commit()

    async def _update_reaction(self, reaction: Reactions, post_id: str):
        """Update user reaction."""
        stmt = (
            update(UsersReactions)
            .where(
                UsersReactions.post_id == post_id
                and self.get_user_id() == UsersReactions.user_id
            )
            .values(reaction=reaction)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def del_reaction(self, post_id: UUID):
        """Delete reaction for post."""
        existing_reaction = await self._check_reaction(post_id)
        if existing_reaction is not None:
            await self._del_reaction(post_id)

    async def _del_reaction(self, post_id: str):
        """Delete reaction from database."""
        stmt = delete(UsersReactions).where(
            UsersReactions.post_id == post_id
            and self.get_user_id() == UsersReactions.user_id
        )
        await self.session.execute(stmt)
        await self.session.commit()


def get_reaction_crud_service(
    token: str = Depends(token_checkout),
    session: AsyncSession = Depends(get_session),
) -> ReactionsCrud:
    return ReactionsCrud(session=session, token=token)
