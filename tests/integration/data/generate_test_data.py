import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.config import get_settings
from schemas.schemas import (
    UserData,
    Users,
    PostsUsers,
    Posts,
    UsersReactions,
    Reaction,
)
from utils.hashed_passwod import hash_password

settings = get_settings()

engine = create_engine("postgresql://app:123@localhost/social")


def set_user(user_data: dict):
    with Session(engine) as session:
        user = Users(
            id=user_data.get("id"),
            login=user_data.get("login"),
            password=hash_password(user_data.get("password")),
            email=user_data.get("email"),
        )
        user_d = UserData(id=uuid.uuid4(), user_id=user.id)
        session.add_all((user, user_d))
        session.commit()


def set_post(post_data: dict):
    with Session(engine) as session:
        post = Posts(id=post_data.get("id"), post=post_data.get("post"))
        posts_users = PostsUsers(
            id=uuid.uuid4(),
            post_id=post.id,
            author_id=post_data.get("author_id"),
        )
        session.add_all((post, posts_users))
        session.commit()


def set_user_reaction(reaction_data: dict):
    with Session(engine) as session:
        user_reaction = UsersReactions(
            id=uuid.uuid4(),
            post_id=reaction_data.get("post_id"),
            user_id=reaction_data.get("user_id"),
            reaction=reaction_data.get("reaction"),
        )
        session.add(user_reaction)
        session.commit()


def set_reactions():
    with Session(engine) as session:
        user_reaction_like = Reaction(id=1, reaction="like")
        user_reaction_dislike = Reaction(id=0, reaction="dislike")
        session.add_all((user_reaction_dislike, user_reaction_like))
        session.commit()


user_1 = {
    "login": "login_1",
    "id": "a9b4aadd-c288-440d-8dc5-50673713b800",
    "password": "password_1",
    "email": "email_1@gmail.com",
}
user_2 = {
    "login": "login_2",
    "id": "a1d40593-242b-46cf-8d4d-4f385ca9a4d3",
    "password": "password_2",
    "email": "email_2@gmail.com",
}
user_3 = {
    "login": "login_3",
    "id": "1340693a-2027-40a4-bcbe-07391b504c35",
    "password": "password_3",
    "email": "email_3@gmail.com",
}

for user in (user_1, user_3, user_2):
    set_user(user)

user_1_post = {
    "author_id": user_1.get("id"),
    "id": "e98dcd1a-c3f8-4a7e-aecd-1547cfa9fd9e",
    "post": "content_1",
}
user_2_post = {
    "author_id": user_2.get("id"),
    "id": "4df9789c-f191-4e6c-a60c-de576a91a47c",
    "post": "content_2",
}
user_3_post = {
    "author_id": user_3.get("id"),
    "id": "c5e7032a-2c7a-4ea0-9e90-cd366d8af2e6",
    "post": "content_3",
}

for post in (user_1_post, user_2_post, user_3_post):
    set_post(post)

set_reactions()
