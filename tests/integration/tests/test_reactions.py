import time
from http import HTTPStatus

import pytest
from psycopg import Cursor
from requests import Session  # type: ignore

from config import get_settings
from data.data_for_test import user_1, user_2_post
from tests_utils.http_requests import (
    login,
    get_user_data_by_user_id,
    add_reaction,
)

sett = get_settings()


@pytest.mark.parametrize(
    "reaction_code, status_code, reaction_name",
    ((1, HTTPStatus.OK, "like"), (0, HTTPStatus.OK, "dislike")),
)
def test_add_reaction(
    http_session: Session,
    reaction_name: str,
    status_code: HTTPStatus,
    postgres_cur: Cursor,
    add_test_data_in_postgres: None,
    reaction_code: int,
) -> None:
    """Test 'add reactions' endpoint."""
    tokens: dict = login(
        http_session,
        {"login": user_1.get("login"), "password": user_1.get("password")},
    )

    access = tokens.get("access_token")
    time.sleep(1)
    post_id = user_2_post.get("id")
    reaction_data = {"post_id": post_id, "reaction": reaction_code}
    user_2_data = get_user_data_by_user_id(
        http_session, user_2_post.get("author_id"), token=access
    )
    reaction = user_2_data.get("posts")[0].get(reaction_name)
    assert reaction == 0

    add_reaction(http_session, reaction_data, access)

    user_2_data = get_user_data_by_user_id(
        http_session, user_2_post.get("author_id"), token=access
    )
    reaction = user_2_data.get("posts")[0].get(reaction_name)
    assert reaction == 1


@pytest.mark.parametrize(
    "token, status_code",
    (
        ("Bearer Wrong token", HTTPStatus.CONFLICT),
        (None, HTTPStatus.FORBIDDEN),
        ("Wrong token", HTTPStatus.FORBIDDEN),
    ),
)
def test_add_reaction_access_error(
    http_session: Session,
    add_test_data_in_postgres: None,
    token: str | None,
    status_code: HTTPStatus,
) -> None:
    """Test access for 'reactions' endpoint."""
    response = http_session.post(
        url=f"{sett.url}reaction",
        headers={"Authorization": token},
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "status_code, body",
    (
        (
            HTTPStatus.NOT_FOUND,
            {"post_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "reaction": 1},
        ),
        (HTTPStatus.UNPROCESSABLE_ENTITY, {"Wrong": "Request", "Format": True}),
        (HTTPStatus.UNPROCESSABLE_ENTITY, None),
    ),
)
def test_add_reaction_error(
    http_session: Session,
    add_test_data_in_postgres: None,
    status_code: HTTPStatus,
    body: dict,
) -> None:
    """Test - wrong request to add reaction."""
    tokens: dict = login(
        http_session,
        {"login": user_1.get("login"), "password": user_1.get("password")},
    )

    access = tokens.get("access_token")
    time.sleep(1)

    response = http_session.post(
        url=f"{sett.url}reaction",
        headers={"Authorization": f"Bearer {access}"},
        json=body,
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "reaction_code, status_code, reaction_name",
    ((1, HTTPStatus.OK, "like"), (0, HTTPStatus.OK, "dislike")),
)
def test_del_reaction(
    http_session: Session,
    reaction_name: str,
    status_code: HTTPStatus,
    postgres_cur: Cursor,
    add_test_data_in_postgres: None,
    reaction_code: int,
) -> None:
    """Test 'delete reactions' endpoint."""
    tokens: dict = login(
        http_session,
        {"login": user_1.get("login"), "password": user_1.get("password")},
    )

    access = tokens.get("access_token")
    time.sleep(1)
    post_id = user_2_post.get("id")
    reaction_data = {"post_id": post_id, "reaction": reaction_code}

    add_reaction(http_session, reaction_data, access)

    reaction_data = {"post_id": post_id, "reaction": -1}

    response = http_session.post(
        url=f"{sett.url}reaction",
        headers={"Authorization": f"Bearer {access}"},
        json=reaction_data,
    )

    assert response.status_code == HTTPStatus.OK

    user_2_data = get_user_data_by_user_id(
        http_session, user_2_post.get("author_id"), token=access
    )
    reaction = user_2_data.get("posts")[0].get(reaction_name)
    assert reaction == 0
