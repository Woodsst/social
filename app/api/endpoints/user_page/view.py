from uuid import UUID

from fastapi import APIRouter, Depends

from api.endpoints.base import Paginator
from api.endpoints.user_page.service import (
    UserPageService,
    get_user_page_service,
)
from models.user_page_models import UserDataInPage

user_router = APIRouter()


@user_router.get(
    path="/",
    description="Get user data for home user page.",
    response_model=UserDataInPage,
)
async def user_home_page(
    service: UserPageService = Depends(get_user_page_service),
    paginator: Paginator = Depends(),
) -> UserDataInPage:
    """User home page view."""
    return await service.get_self_data(
        paginator.page_size, paginator.page_number
    )


@user_router.get(
    path="/user", description="Get user page.", response_model=UserDataInPage
)
async def user_page(
    paginator: Paginator = Depends(),
    service: UserPageService = Depends(get_user_page_service),
    id: UUID | None = None,
) -> UserDataInPage:
    """User page request by id."""
    return await service.get_user_data(
        id, page_size=paginator.page_size, page_number=paginator.page_number
    )
