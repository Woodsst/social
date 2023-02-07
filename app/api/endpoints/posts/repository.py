from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas import Posts


class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_post(self, content: str, author: str) -> None:
        """Added post in database."""
        post = Posts(post=content, author_id=author)
        self.session.add(post)
        await self.session.commit()
