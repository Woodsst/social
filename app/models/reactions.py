from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Reactions(str, Enum):
    like = "like"
    dislike = "dislike"


class Reaction(BaseModel):
    """Model for user reaction to post."""

    post_id: UUID
    reaction: Reactions
