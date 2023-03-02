import time
from http import HTTPStatus

import pytest
from psycopg import Cursor
from requests import Session, post

from tests_utils.http_requests import login, get_user_data
from data.data_for_test import user_1
from config import get_settings

sett = get_settings()


def test_add_post(
        postgres_cur: Cursor, http_session: Session, add_test_data_in_postgres: None
):
    """Test - add post."""

    tokens: dict = login(
        http_session,
        {"login": user_1.get("login"), "password": user_1.get("password")},
    )

    access = tokens.get("access_token")
    time.sleep(1)
    content = "Test post 1"
    body = {"content": content}

    response = post(
        url=f"{sett.url}post/add",
        headers={"Authorization": f"Bearer {access}"},
        json=body,
    )

    assert response.status_code == HTTPStatus.OK

    user_data: dict = get_user_data(http_session, access)

    user_posts: list = user_data.get("posts")

    assert user_posts[0].get("content") == content


@pytest.mark.parametrize(
    "token, status_code",
    (
            ("Bearer Wrong token", HTTPStatus.CONFLICT),
            (None, HTTPStatus.FORBIDDEN),
            ("Wrong token", HTTPStatus.FORBIDDEN)
    )
)
def test_add_posts_error(
        postgres_cur: Cursor,
        http_session: Session,
        add_test_data_in_postgres: None,
        token: str | None,
        status_code: HTTPStatus
):
    """Test - wrong request to add new post."""

    content = "Test post 1"
    body = {"content": content}

    response = post(
        url=f"{sett.url}post/add",
        headers={"Authorization": token},
        json=body,
    )

    assert response.status_code == status_code
