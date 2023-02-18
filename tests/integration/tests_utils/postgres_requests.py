from psycopg import Cursor


def get_user_data(cursor: Cursor, user_name: str) -> tuple:
    """Getting user data to user name"""

    sql = """
        SELECT *
        FROM users
        WHERE name = %s
    """

    cursor.execute(sql, (user_name,))

    return cursor.fetchone()
