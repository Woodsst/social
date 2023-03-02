import time
from http import HTTPStatus

import pytest
from psycopg import Cursor
from requests import Session, post

from tests_utils.http_requests import login, get_user_data, add_post
from data.data_for_test import user_1, user_1_post
from config import get_settings
from tests_utils.postgres_requests import get_post_by_id

sett = get_settings()


def test_add_post(http_session: Session, add_test_data_in_postgres: None):
    """Test - add post."""

    tokens: dict = login(
        http_session,
        {"login": user_1.get("login"), "password": user_1.get("password")},
    )

    access = tokens.get("access_token")
    time.sleep(1)
    content = "Test post 1"
    post_data = {"content": content}

    user_data: dict = get_user_data(http_session, access)
    assert len(user_data.get("posts")) == 1

    add_post(http_session, access, post_data)
    user_data: dict = get_user_data(http_session, access)
    assert len(user_data.get("posts")) == 2

    content_count = [post.get("content") for post in user_data.get("posts")]
    assert content in content_count


@pytest.mark.parametrize(
    "token, status_code",
    (
        ("Bearer Wrong token", HTTPStatus.CONFLICT),
        (None, HTTPStatus.FORBIDDEN),
        ("Wrong token", HTTPStatus.FORBIDDEN),
    ),
)
def test_add_posts_error(
    http_session: Session,
    add_test_data_in_postgres: None,
    token: str | None,
    status_code: HTTPStatus,
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


def test_edit_post(
    postgres_cur: Cursor, http_session: Session, add_test_data_in_postgres: None
):
    """Test - edit post."""

    tokens: dict = login(
        http_session,
        {"login": user_1.get("login"), "password": user_1.get("password")},
    )

    access = tokens.get("access_token")
    time.sleep(1)

    content = "Test post 1"
    post_data = {"content": content}

    add_post(http_session, access, post_data)
    user_data: dict = get_user_data(http_session, access)
    user_posts: list = user_data.get("posts")
    post_id = user_posts[1].get("id")
    post_for_edit_request_body = {"content": "Edited post", "post_id": post_id}

    response = http_session.patch(
        url=f"{sett.url}post/edit",
        headers={"Authorization": f"Bearer {access}"},
        json=post_for_edit_request_body,
    )

    assert response.status_code == HTTPStatus.OK

    post_data_from_db: dict = get_post_by_id(postgres_cur, post_id)

    assert post_data_from_db.get("post") == post_for_edit_request_body.get(
        "content"
    )


@pytest.mark.parametrize(
    "token, status_code",
    (
        ("Bearer Wrong token", HTTPStatus.CONFLICT),
        (None, HTTPStatus.FORBIDDEN),
        ("Wrong token", HTTPStatus.FORBIDDEN),
    ),
)
def test_edit_post_access_error(
    http_session: Session,
    add_test_data_in_postgres: None,
    token: str | None,
    status_code: HTTPStatus,
):
    """Test - access error to 'edit post' endpoint."""

    response = http_session.patch(
        url=f"{sett.url}post/edit",
        headers={"Authorization": token},
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "status_code, body",
    (
        (
            HTTPStatus.NOT_FOUND,
            {
                "content": "new content",
                "post_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            },
        ),
        (HTTPStatus.UNPROCESSABLE_ENTITY, {"Wrong": "Request", "Format": True}),
        (HTTPStatus.UNPROCESSABLE_ENTITY, None),
    ),
)
def test_edit_post_request_error(
    http_session: Session,
    add_test_data_in_postgres: None,
    status_code: HTTPStatus,
    body: dict | None,
):
    """Test - wrong request to edit post."""

    tokens: dict = login(
        http_session,
        {"login": user_1.get("login"), "password": user_1.get("password")},
    )

    access = tokens.get("access_token")
    time.sleep(1)

    response = http_session.patch(
        url=f"{sett.url}post/edit",
        headers={"Authorization": f"Bearer {access}"},
        json=body,
    )

    assert response.status_code == status_code


def test_delete_post(
    postgres_cur: Cursor, http_session: Session, add_test_data_in_postgres: None
):
    """Test for delete post endpoint."""

    tokens: dict = login(
        http_session,
        {"login": user_1.get("login"), "password": user_1.get("password")},
    )

    access = tokens.get("access_token")
    time.sleep(1)

    user_data: dict = get_user_data(http_session, access)
    assert len(user_data.get("posts")) == 1

    response = http_session.delete(
        url=f"{sett.url}post/delete?post_id={user_1_post.get('id')}",
        headers={"Authorization": f"Bearer {access}"},
    )

    assert response.status_code == HTTPStatus.OK

    user_data: dict = get_user_data(http_session, access)
    assert len(user_data.get("posts")) == 0


@pytest.mark.parametrize(
    "token, status_code",
    (
        ("Bearer Wrong token", HTTPStatus.CONFLICT),
        (None, HTTPStatus.FORBIDDEN),
        ("Wrong token", HTTPStatus.FORBIDDEN),
    ),
)
def test_delete_post_access_error(
    http_session: Session,
    add_test_data_in_postgres: None,
    status_code: HTTPStatus,
    token: str | None,
):
    """Test access error for 'delete post' endpoint."""

    response = http_session.patch(
        url=f"{sett.url}post/edit",
        headers={"Authorization": token},
    )

    assert response.status_code == status_code


def test_delete_post_delete_error(
    http_session: Session,
    add_test_data_in_postgres: None,
):
    """Test access error for 'delete post' endpoint."""

    tokens: dict = login(
        http_session,
        {"login": user_1.get("login"), "password": user_1.get("password")},
    )

    access = tokens.get("access_token")
    time.sleep(1)
    other_user_post_id = "4df9789c-f191-4e6c-a60c-de576a91a47c"
    response = http_session.delete(
        url=f"{sett.url}post/delete?post_id={other_user_post_id}",
        headers={"Authorization": f"Bearer {access}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
