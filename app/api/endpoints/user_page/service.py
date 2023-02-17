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
    """Service for working with user data."""

    def __init__(self, token: str, repo: BaseUserPageRepository):
        super().__init__(token)
        self.repo = repo

    async def get_user_data(self, user_id: UUID, page_size: int, page_number: int) -> UserDataInPage:
        """Getting user data by user id."""
        user_data = await self.repo.get_user_data(user_id)
        name, sur_name, date_of_birth = user_data
        raw_posts = await self.repo.get_user_posts(user_id, page_size=page_size, page_number=page_number)
        return UserDataInPage(
            user_name=name,
            user_surname=sur_name,
            date_of_birth=date_of_birth,
            posts=[
                Post(
                    id=str(post._mapping.get("id")),
                    author=name,
                    content=post._mapping.get("content"),
                    like=post._mapping.get("like"),
                    dislike=post._mapping.get("dislike"),
                    create_at=post._mapping.get("create_at"),
                )
                for post in raw_posts
            ],
        )

    async def get_self_data(self, page_size: int, page_number: int) -> UserDataInPage:
        payload: dict = decode_access_token(self.token)
        user_id = payload.get("sub")
        return await self.get_user_data(user_id, page_size, page_number)


def get_user_page_service(
    token: str = Depends(token_checkout),
    repo: BaseUserPageRepository = Depends(get_user_page_repo),
) -> UserPageService:
    return UserPageService(repo=repo, token=token)
