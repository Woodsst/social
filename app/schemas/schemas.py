import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UsersReactions(Base):
    __tablename__ = "users_reaction"

    id = Column(UUID(as_uuid=True), primary_key=True)
    post_id = Column(ForeignKey("posts.id"), nullable=False)
    r_like = Column(UUID(as_uuid=True))
    r_dislike = Column(UUID(as_uuid=True))


class Posts(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True)
    post = Column(String, nullable=False)
    create_at = Column(DateTime, default=datetime.datetime.now())
    author_id = Column(ForeignKey("users.id"))

    users_reactions = relationship(UsersReactions)


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    create_at = Column(DateTime, default=datetime.datetime.now())
    name = Column(String, nullable=False)
    sur_name = Column(String)
    date_of_birth = Column(DateTime)

    users_posts = relationship(Posts)
