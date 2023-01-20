from http import HTTPStatus

from fastapi import APIRouter, Depends

from api.endpoints.reaction.service import (
    ReactionsCrud,
    get_reaction_crud_service,
)
from models.reactions import Reaction, Reactions
from starlette.exceptions import HTTPException

user_reaction = APIRouter()


@user_reaction.post(
    path="/",
    description="add reaction.",
)
async def add_reaction_for_post(
    reaction: Reaction,
    service: ReactionsCrud = Depends(get_reaction_crud_service),
):
    """Add reaction view."""
    if reaction.reaction == Reactions.like:
        if await service.add_like(reaction.post_id):
            return HTTPStatus.OK
        else:
            raise HTTPException(HTTPStatus.CONFLICT)

    elif reaction.reaction == Reactions.dislike:
        if await service.add_dislike(reaction.post_id):
            return HTTPStatus.OK
        else:
            raise HTTPException(HTTPStatus.CONFLICT)

    else:
        await service.del_reaction(reaction.post_id)
