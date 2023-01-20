from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Reactions(int, Enum):
    """Reactions enum where like = 1 dislike = 0."""

    like = 1
    dislike = 0


class Reaction(BaseModel):
    """Model for user reaction to post."""

    post_id: UUID
    reaction: Reactions
