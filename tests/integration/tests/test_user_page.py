import time
from http import HTTPStatus

import pytest
from psycopg import Cursor
from requests import Session  # type: ignore

from config import get_settings
from data.data_for_test import user_1, user_1_post
from tests_utils.http_requests import login

sett = get_settings()


def test_get_user_page(
    postgres_cur: Cursor, http_session: Session, add_test_data_in_postgres: None
) -> None:
    """Test - correctly working user_page endpoint."""
    tokens: dict = login(
        http_session,
        {"login": user_1.get("login"), "password": user_1.get("password")},
    )
    access = tokens.get("access_token")
    time.sleep(1)

    response = http_session.get(
        url=f"{sett.url}user/home?page_size=10&page_number=0",
        headers={
            "Authorization": f"Bearer {access}",
            "accept": "application/json",
        },
    )

    payload: dict = response.json()
    posts = payload.get("posts")

    assert response.status_code == HTTPStatus.OK
    assert user_1.get("name") == payload.get("user_name")
    assert len(posts) == 1
    assert posts[0].get("id") == user_1_post.get("id")
    assert posts[0].get("content") == user_1_post.get("post")


@pytest.mark.parametrize(
    "token, status_code",
    (
        (
            {
                "accept": "application/json",
                "Authorization": "Bearer bad_token",
            },
            HTTPStatus.CONFLICT,
        ),
        (None, HTTPStatus.FORBIDDEN),
    ),
)
def test_get_user_page_access_denied(
    token: str | None,
    status_code: HTTPStatus,
    http_session: Session,
    add_test_data_in_postgres: None,
) -> None:
    """Test - access for user_page endpoint."""
    response = http_session.get(
        url=f"{sett.url}user/home?page_size=10&page_number=0", headers=token
    )

    assert response.status_code == status_code
