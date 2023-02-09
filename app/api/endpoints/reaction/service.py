from uuid import UUID

from fastapi import Depends

from api.endpoints.base import ServiceWithToken
from api.endpoints.reaction.repository import (
    BaseReactionsRepository,
    get_reactions_repo,
)
from models.reactions import Reactions
from utils.tokens import token_checkout


class ReactionsCrud(ServiceWithToken):
    """CRUD for reactions to post."""

    def __init__(self, repo: BaseReactionsRepository, token: str):
        super().__init__(token)
        self.repo = repo

    async def add_reaction(self, reaction: Reactions, post_id: str):
        """Add reaction from user."""
        user_id = self.get_user_id()
        existing_reaction = await self.repo.check_reaction(post_id, user_id)
        if existing_reaction is None:
            await self.repo.add_reaction(reaction, post_id, user_id)
        elif existing_reaction != reaction:
            await self.repo.update_reaction(reaction, post_id, user_id)
            return True
        return False

    async def del_reaction(self, post_id: UUID):
        """Delete reaction for post."""
        existing_reaction = await self.repo.check_reaction(
            post_id, self.get_user_id()
        )
        if existing_reaction is not None:
            await self.repo.del_reaction(post_id, self.get_user_id())


def get_reaction_crud_service(
    token: str = Depends(token_checkout),
    repo: BaseReactionsRepository = Depends(get_reactions_repo),
) -> ReactionsCrud:
    return ReactionsCrud(repo=repo, token=token)
