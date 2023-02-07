from fastapi import APIRouter

posts = APIRouter()


@posts.post(
    path="/",
    description="Add new post.",
)
async def add_post():
    """View for add new post."""
