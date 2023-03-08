import datetime
import uuid

from psycopg import Cursor

from data.data_for_test import (
    user_1,
    user_3,
    user_2,
    user_1_post,
    user_3_post,
    user_2_post,
)
from tests_utils.hashed_password import hash_password


def add_user(user_data: dict, cursor: Cursor) -> None:
    """Add test users."""
    sql = """
    INSERT INTO users (id, login, password, email, name)
    VALUES (%s,%s,%s,%s,%s)
    """

    cursor.execute(
        sql,
        (
            user_data.get("id"),
            user_data.get("login"),
            hash_password(user_data.get("password")),
            user_data.get("email"),
            user_data.get("name"),
        ),
    )
    cursor.connection.commit()


def add_post(post_data: dict, cursor: Cursor) -> None:
    """Add test posts."""
    sql = """
    INSERT INTO posts (id, post, author_id, create_at)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(
        sql,
        (
            post_data.get("id"),
            post_data.get("post"),
            post_data.get("author_id"),
            datetime.datetime.now(),
        ),
    )
    cursor.connection.commit()


def add_user_reaction(reaction_data: dict, cursor: Cursor) -> None:
    """Add test users reactions."""
    sql = """
    INSERT INTO users_reaction (post_id, user_id, reaction)
    VALUES (%s,%s,%s)
    """
    cursor.execute(
        sql,
        (
            uuid.uuid4(),
            reaction_data.get("post_id"),
            reaction_data.get("user_id"),
            reaction_data.get("reaction"),
        ),
    )
    cursor.connection.commit()


def add_like_and_dislike(cursor: Cursor) -> None:
    """Add like and dislike to test posts."""
    sql = """
    INSERT INTO users_reaction (id, post_id, r_like)
    VALUES (%s,%s,%s)
    """
    cursor.execute(
        sql,
        (
            uuid.uuid4(),
            "e98dcd1a-c3f8-4a7e-aecd-1547cfa9fd9e",
            "a1d40593-242b-46cf-8d4d-4f385ca9a4d3",
        ),
    )
    sql = """
    INSERT INTO users_reaction (id, post_id, r_dislike)
    VALUES (%s,%s,%s)
    """
    cursor.execute(
        sql,
        (
            uuid.uuid4(),
            "e98dcd1a-c3f8-4a7e-aecd-1547cfa9fd9e",
            "1340693a-2027-40a4-bcbe-07391b504c35",
        ),
    )
    cursor.connection.commit()


def add_test_data(cursor: Cursor) -> None:
    """Add all test data in postgres."""
    for user in (user_1, user_3, user_2):
        add_user(user, cursor)

    for post in (user_1_post, user_2_post, user_3_post):
        add_post(post, cursor)

    add_like_and_dislike(cursor)


def delete_data(cursor: Cursor) -> None:
    sql = """
    DELETE FROM users_reaction;
    DELETE FROM posts;
    DELETE FROM users;
    """
    cursor.execute(sql)
    cursor.connection.commit()
