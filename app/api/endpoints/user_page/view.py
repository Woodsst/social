from uuid import UUID

from fastapi import APIRouter, Depends

from api.endpoints.user_page.service import (
    UserPageService,
    get_user_page_service,
)

user_router = APIRouter()


@user_router.get(
    path="/",
    description="Get user data for home user page.",
)
async def user_home_page(
    service: UserPageService = Depends(get_user_page_service),
):
    """User home page view."""
    return await service.get_user_data_from_token()


@user_router.get(
    path="/user",
    description="Get user page.",
)
async def user_page(
    service: UserPageService = Depends(get_user_page_service),
    id: UUID = None,
):
    """User page request by id."""
    return await service.get_user_data(id)
