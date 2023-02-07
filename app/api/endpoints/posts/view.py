from fastapi import APIRouter, Depends

from api.endpoints.posts.service import PostsCrud, get_posts_crud_service
from models.user_page_models import CreatePost

posts = APIRouter()


@posts.post(
    path="/add",
    description="Add new post.",
)
async def add_post(
    post: CreatePost, service: PostsCrud = Depends(get_posts_crud_service)
):
    """View for add new post."""
    await service.add(post)
    return {"message": "ok"}
