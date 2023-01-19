from fastapi import APIRouter, Depends

from api.endpoints.user_page.service import (
    UserPageService,
    get_user_page_service,
)

user_router = APIRouter()


@user_router.get(
    path="/",
    description="Reqeust for registration",
)
async def user_home_page(
    service: UserPageService = Depends(get_user_page_service),
):
    """User home page view."""
    return await service.get_user_data()
