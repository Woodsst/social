import uuid

from psycopg import Cursor

from data.data_for_test import user_1, user_3, user_2
from tests_utils.hashed_password import hash_password


def add_user(user_data: dict, cursor: Cursor):
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


def add_post(post_data: dict, cursor: Cursor):
    """Add test posts."""

    sql = """
    INSERT INTO posts (id, post, author_id)
    VALUES (%s,%s,%s)
    """
    cursor.execute(
        sql,
        (
            post_data.get("id"),
            post_data.get("post"),
            post_data.get("author_id"),
        ),
    )
    cursor.connection.commit()


def add_user_reaction(reaction_data: dict, cursor: Cursor):
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


def add_like_and_dislike(cursor: Cursor):
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


def add_test_data(cursor: Cursor):
    """Add all test data in postgres"""

    for user in (user_1, user_3, user_2):
        add_user(user, cursor)

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
        add_post(post, cursor)

    add_like_and_dislike(cursor)


def delete_data(cursor: Cursor):
    sql = """
    DELETE FROM users_reaction;
    DELETE FROM posts;
    DELETE FROM users;
    """
    cursor.execute(sql)
    cursor.connection.commit()
