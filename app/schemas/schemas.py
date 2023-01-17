import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class PostsUsers(Base):
    __tablename__ = "posts_users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    author_id = Column(ForeignKey("users.id"), nullable=False)
    post_id = Column(ForeignKey("posts.id"), nullable=False)


class UserData(Base):
    __tablename__ = "users_data"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    name = Column(String)
    sur_name = Column(String)
    date_of_birth = Column(DateTime)


class UsersReactions(Base):
    __tablename__ = "users_reaction"

    id = Column(UUID(as_uuid=True), primary_key=True)
    post_id = Column(ForeignKey("posts.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    reaction = Column(ForeignKey("reaction.id"))


class Reaction(Base):
    __tablename__ = "reaction"

    id = Column(Integer, primary_key=True)
    reaction = Column(String, nullable=False)

    posts_users = relationship(UsersReactions)


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    create_date = Column(DateTime, default=datetime.datetime.now())

    user_data = relationship(UserData)
    posts_users = relationship(PostsUsers)
    users_reaction = relationship(UsersReactions)


class Posts(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True)
    post = Column(String, nullable=False)

    posts_users = relationship(PostsUsers)
