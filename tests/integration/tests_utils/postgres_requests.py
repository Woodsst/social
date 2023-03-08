from typing import Optional, Any

from psycopg import Cursor


def get_user_data(cursor: Cursor, user_name: str) -> Optional[Any]:
    """Getting user data to user name."""
    sql = """
        SELECT *
        FROM users
        WHERE name = %s
    """

    cursor.execute(sql, (user_name,))

    return cursor.fetchone()


def get_post_by_id(cursor: Cursor, post_id: str) -> Optional[Any]:
    """Getting post data by post id."""
    sql = """
    SELECT *
    FROM posts
    WHERE id = %s
    """

    cursor.execute(sql, (post_id,))

    return cursor.fetchone()
