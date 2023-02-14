from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints.base import ServiceWithToken
from api.endpoints.posts.repository import (
    BasePostRepository,
    PostPostgresRepository,
)
from db.get_session import get_session
from models.user_page_models import CreatePost, EditPost
from utils.tokens import token_checkout


class PostsCrud(ServiceWithToken):
    """CRUD for posts."""

    def __init__(self, repo: BasePostRepository, token: str):
        super().__init__(token)
        self.repo = repo

    async def add(self, post: CreatePost):
        """Add new post."""
        await self.repo.add_post(
            content=post.content, author=self.get_user_id()
        )

    async def edit(self, post: EditPost):
        """Edit exist post."""
        await self.repo.edit_post(post.content, str(post.post_id))

    async def delete(self, post_id: UUID):
        """Delete post."""


def get_posts_crud_service(
    token: str = Depends(token_checkout),
    session: AsyncSession = Depends(get_session),
) -> PostsCrud:
    return PostsCrud(repo=PostPostgresRepository(session), token=token)
