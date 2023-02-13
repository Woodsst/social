from uuid import UUID

from fastapi import APIRouter, Depends

from api.endpoints.user_page.service import (
    UserPageService,
    get_user_page_service,
)
from models.user_page_models import UserDataInPage

user_router = APIRouter()


@user_router.get(
    path="/",
    description="Get user data for home user page.",
    response_model=UserDataInPage
)
async def user_home_page(
    service: UserPageService = Depends(get_user_page_service),
):
    """User home page view."""
    return await service.get_self_data()


@user_router.get(
    path="/user",
    description="Get user page.",
    response_model=UserDataInPage
)
async def user_page(
    service: UserPageService = Depends(get_user_page_service),
    id: UUID = None,
):
    """User page request by id."""
    return await service.get_user_data(id)
