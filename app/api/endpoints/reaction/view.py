from fastapi import APIRouter, Depends

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
):
    """Add reaction view."""
    if reaction.reaction == Reactions.like:
        await service.add_like(reaction.post_id)

    elif reaction.reaction == Reactions.dislike:
        await service.add_dislike(reaction.post_id)

    else:
        await service.del_reaction(reaction.post_id)
