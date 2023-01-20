from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints.base import ServiceWithToken
from db.get_session import get_session
from utils.tokens import token_checkout


class ReactionsCrud(ServiceWithToken):
    """CRUD for reactions to post."""

    async def add_like(self, post_id: UUID):
        """Add like for post."""

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
