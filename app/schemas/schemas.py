import uuid

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    login = Column(String)
    password = Column(String)
    create_date = Column(DateTime)
    user_data = relationship("user_data")
    posts_users = relationship("posts_users")
    users_reaction = relationship("users_reaction")


class UserData(Base):
    __tablename__ = "users_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    user_id = Column(ForeignKey("users.id"))
    name = Column(String)
    sur_name = Column(String)
    family = Column(String)
    date_of_birth = Column(DateTime)


class Posts(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    post = Column(String)


class PostsUsers(Base):
    __tablename__ = "posts_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    id_author = Column(ForeignKey("users.id"))
    id_post = Column(ForeignKey("posts.id"))


class Reaction(Base):
    __tablename__ = "reaction"

    id = Column(Integer, primary_key=True)
    Reaction = Column(String)


class UsersReactions(Base):
    __tablename__ = "users_reaction"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    id_post = Column(ForeignKey("posts.id"))
    id_user = Column(ForeignKey("users.id"))
    reaction = Column(ForeignKey("reaction.id"))
