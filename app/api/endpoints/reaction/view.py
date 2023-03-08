from http import HTTPStatus

from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException

from api.endpoints.reaction.service import (
    ReactionsCrud,
    get_reaction_crud_service,
)
from models.reactions import Reaction, Reactions

user_reaction = APIRouter()


@user_reaction.post(
    path="/",
    description="add reaction.",
)
async def add_reaction_for_post(
    reaction: Reaction,
    service: ReactionsCrud = Depends(get_reaction_crud_service),
) -> HTTPStatus:
    """Add reaction view."""
    if reaction.reaction == Reactions.drop_reaction:
        await service.del_reaction(reaction.post_id)
        return HTTPStatus.OK

    if await service.add_reaction(reaction.reaction, reaction.post_id):
        return HTTPStatus.OK
    raise HTTPException(HTTPStatus.CONFLICT)
