import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class PostsUsers(Base):
    __tablename__ = "posts_users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    id_author = Column(ForeignKey("users.id"))
    id_post = Column(ForeignKey("posts.id"))


class UserData(Base):
    __tablename__ = "users_data"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    name = Column(String)
    sur_name = Column(String)
    family = Column(String)
    date_of_birth = Column(DateTime)


class Reaction(Base):
    __tablename__ = "reaction"

    id = Column(Integer, primary_key=True)
    Reaction = Column(String)


class UsersReactions(Base):
    __tablename__ = "users_reaction"

    id = Column(UUID(as_uuid=True), primary_key=True)
    id_post = Column(ForeignKey("posts.id"))
    id_user = Column(ForeignKey("users.id"))
    reaction = Column(ForeignKey("reaction.id"))


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    create_date = Column(DateTime, default=datetime.datetime.now())

    user_data = relationship(UserData)
    posts_users = relationship(PostsUsers)
    users_reaction = relationship(UsersReactions)


class Posts(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True)
    post = Column(String)
