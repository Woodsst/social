from typing import List
from uuid import UUID

from fastapi import Depends

from api.endpoints.base import ServiceWithToken
from api.endpoints.user_page.repository import (
    BaseUserPageRepository,
    get_user_page_repo,
)
from models.user_page_models import Post, UserDataInPage
from utils.tokens import decode_access_token, token_checkout


class UserPageService(ServiceWithToken):
    def __init__(self, token: str, repo: BaseUserPageRepository):
        super().__init__(token)
        self.repo = repo

    async def get_user_data(
        self, other_user_id: UUID | None = None
    ) -> UserDataInPage:
        """Getting user data by user id."""
        payload: dict = decode_access_token(self.token)
        user_id = payload.get("sub")
        if other_user_id:
            user_data = await self.repo.get_user_data(other_user_id)
        user_data = await self.repo.get_user_data(user_id)
        name, sur_name, date_of_birth = user_data
        raw_posts = await self.repo.get_user_posts(user_id, name)
        posts = create_posts(raw_posts, name)
        return UserDataInPage(
            user_name=name,
            user_surname=sur_name,
            date_of_birth=date_of_birth,
            posts=posts,
        )


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
    repo: BaseUserPageRepository = Depends(get_user_page_repo),
) -> UserPageService:
    return UserPageService(repo=repo, token=token)
