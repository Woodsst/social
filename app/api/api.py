from fastapi import APIRouter

from api.endpoints.login.view import login_router
from api.endpoints.posts.view import posts
from api.endpoints.reaction.view import user_reaction
from api.endpoints.registration.view import registration_router
from api.endpoints.user_page.view import user_router

api_router = APIRouter()

api_router.include_router(login_router, prefix="/login", tags=["Authorization"])
api_router.include_router(
    registration_router,
    prefix="/registration",
    tags=["Authorization"],
)
api_router.include_router(user_router, tags=["User Page"])
api_router.include_router(
    user_reaction,
    prefix="/reaction",
    tags=["User reactions"],
)
api_router.include_router(posts, prefix="/post", tags=["Posts CRUD"])
