import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class Post(BaseModel):
    """Model for post in page."""

    id: str
    author: str
    content: str
    like: int
    dislike: int
    create_at: datetime.datetime


class UserDataInPage(BaseModel):
    """Model for all user data."""

    user_name: Optional[str]
    user_surname: Optional[str]
    date_of_birth: Optional[str]
    posts: Optional[List[Post]]


class CreatePost(BaseModel):
    """Model for new post create."""

    content: str
