from uuid import UUID

from fastapi import APIRouter, Depends

from api.endpoints.posts.service import PostsCrud, get_posts_crud_service
from models.user_page_models import CreatePost, EditPost

posts = APIRouter()


@posts.post(
    path="/add",
    description="Add new post.",
)
async def add_post(
    post: CreatePost, service: PostsCrud = Depends(get_posts_crud_service)
) -> dict:
    """View for add new post."""
    await service.add(post)
    return {"message": "ok"}


@posts.patch(path="/edit", description="Edit post")
async def edit_post(
    post: EditPost,
    service: PostsCrud = Depends(get_posts_crud_service),
) -> dict:
    """View for edit post."""
    await service.edit(post)
    return {"message": "ok"}


@posts.delete(path="/delete", description="Delete post")
async def delete_post(
    post_id: UUID, service: PostsCrud = Depends(get_posts_crud_service)
) -> dict:
    """View for delete post."""
    await service.delete(post_id)
    return {"message": "ok"}
