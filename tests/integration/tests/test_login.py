from http import HTTPStatus

import pytest
from requests import Session

from config import get_settings
from tests_utils.http_requests import registration, login
from data.data_for_test import (
    user_data_for_registration,
    user_data_for_login,
    correct_login_status,
)

sett = get_settings()


def test_login(http_session: Session, clear_postgres):
    """Test - worked login endpoint."""
    registration(http_session, user_data_for_registration)

    tokens: dict = login(http_session, user_data_for_login)

    correct_keys = ["access_token", "refresh_token", "login_status"]

    assert isinstance(tokens, dict)

    assert tokens.get("login_status") == correct_login_status

    for key in tokens.keys():
        assert key in correct_keys


@pytest.mark.parametrize(
    "user_data, status_code",
    (
        ({"login": "wrong_login", "password": "password"}, HTTPStatus.CONFLICT),
        (
            {
                "wrong_format": "wrong_login",
            },
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ),
)
def test_login_error(
    http_session: Session, clear_postgres, user_data, status_code
):
    """Test - worked login endpoint with uncorrected data from user."""
    registration(http_session, user_data_for_registration)

    response = http_session.post(
        url=f"{sett.url}login/",
        json=user_data,
    )

    assert response.status_code == status_code
