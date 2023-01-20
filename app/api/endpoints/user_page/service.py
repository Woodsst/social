from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.endpoints.base import BaseService
from core.exceptions.user_exeptions import UserNotFound
from db.get_session import get_session
from models.user_page_models import Post, UserDataInPage
from schemas.schemas import Posts, Users, UsersReactions
from utils.tokens import decode_access_token, token_checkout


class UserPageService(BaseService):
    def __init__(self, session: AsyncSession, token: str):
        super().__init__(session=session)
        self.token = token

    async def get_user_data_from_token(self) -> UserDataInPage:
        """Getting user data by user id."""
        payload: dict = decode_access_token(self.token)
        user_id = payload.get("sub")
        return await self.get_user_data(user_id)

    async def get_user_data(self, user_id: str) -> UserDataInPage:
        """Request to the database to receive user data."""
        stmt = select(Users.name, Users.sur_name, Users.date_of_birth).where(
            Users.id == user_id
        )
        reqeust = await self.session.execute(stmt)
        user_data = reqeust.first()
        if user_data is None:
            raise UserNotFound()
        name, sur_name, date_of_birth = user_data
        posts = await self._get_user_posts(user_id, name)
        user_data = UserDataInPage(
            user_name=name,
            user_surname=sur_name,
            date_of_birth=date_of_birth,
            posts=posts,
        )
        return user_data

    async def _get_user_posts(
        self, user_id: str, author_name: str
    ) -> List[Posts]:
        """Request to the database to receive user posts."""
        stmt = (
            select(Posts.post, UsersReactions.reaction)
            .join(UsersReactions)
            .where(
                user_id == Posts.author_id
                and Posts.id == UsersReactions.post_id
            )
            .order_by(Posts.create_at)
        )
        request = await self.session.execute(stmt)
        raw_posts = request.all()
        if len(raw_posts) == 0:
            return raw_posts
        return await create_posts(raw_posts, author_name)


async def create_posts(raw_posts: list, name: str) -> List[Post]:
    """Creating Post Models from raw data."""
    posts = []
    first_post = Post(
        content=raw_posts[0][0],
        author=name,
        like=0,
        dislike=0,
    )
    for index, post in enumerate(raw_posts):
        content, reactions = post
        if content == first_post.content:
            if reactions == 1:
                first_post.like += 1
            else:
                first_post.dislike += 1
        else:
            posts.append(first_post)
            first_post = Post(
                content=content,
                author=name,
                like=0,
                dislike=0,
            )
            if reactions == 1:
                first_post.like += 1
            else:
                first_post.dislike += 1
        if index == len(raw_posts) - 1:
            posts.append(first_post)

    return posts


def get_user_page_service(
    token: str = Depends(token_checkout),
    session: AsyncSession = Depends(get_session),
) -> UserPageService:
    return UserPageService(session=session, token=token)
