import datetime
from abc import ABC, abstractmethod
from uuid import uuid4

from sqlalchemy import update, delete
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas import Posts


class BasePostRepository(ABC):
    """Abstract class for a repository with users posts."""

    @abstractmethod
    async def add_post(self, content: str, author: str) -> None:
        """Add new post."""

    @abstractmethod
    async def edit_post(self, content: str, post_id: str, author_id: str) -> None:
        """Edit post."""

    @abstractmethod
    async def delete_post(self, post_id: str, author_id: str) -> None:
        """Delete post."""


class PostPostgresRepository(BasePostRepository):
    """Interface for working with postgres db for posts."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_post(self, content: str, author: str) -> None:
        """Added post."""
        post = Posts(
            id=uuid4(),
            post=content,
            author_id=author,
            create_at=datetime.datetime.now(),
        )
        self.session.add(post)
        await self.session.commit()

    async def edit_post(self, content: str, post_id: str, author_id: str) -> None:
        """Edit post."""
        stmt = update(Posts).where(Posts.id == post_id, Posts.author_id == author_id).values(post=content)
        result: CursorResult = await self.session.execute(stmt)
        if result.rowcount != 1:
            await self.session.rollback()
            return False
        await self.session.commit()
        return True

    async def delete_post(self, post_id: str, author_id: str) -> None:
        """Delete post."""
        stmt = delete(Posts).where(Posts.id == post_id, Posts.author_id == author_id)
        result: CursorResult = await self.session.execute(stmt)
        if result.rowcount != 1:
            await self.session.rollback()
            return False
        await self.session.commit()
        return True
