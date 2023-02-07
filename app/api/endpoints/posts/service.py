from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints.base import ServiceWithToken
from db.get_session import get_session
from utils.tokens import token_checkout


class PostsCrud(ServiceWithToken):
    """CRUD for posts."""

    async def add(self, post_id: UUID):
        """Add new post."""

    async def edit(self, post_id: UUID):
        """Edit exist post."""

    async def delete(self, post_id: UUID):
        """Delete post."""


def get_reaction_crud_service(
    token: str = Depends(token_checkout),
    session: AsyncSession = Depends(get_session),
) -> PostsCrud:
    return PostsCrud(session=session, token=token)
