from fastapi import APIRouter

from app.api.endpoints.login.view import login_router
from app.api.endpoints.registration.view import registration_router
from app.api.endpoints.user_page.view import user_router

api_router = APIRouter()

api_router.include_router(login_router, prefix="/login", tags=["Authorization"])
api_router.include_router(
    registration_router, prefix="/registration", tags=["Authorization"]
)
api_router.include_router(user_router, tags=["User Page"])
