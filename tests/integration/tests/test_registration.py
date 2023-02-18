from http import HTTPStatus

from psycopg import Cursor
from requests import Session

from config import get_settings
from tests_utils.postgres_requests import get_user_data

sett = get_settings()


def test_registration(
    postgres_cur: Cursor, http_session: Session, clear_postgres
):
    """Test - correctly working registration endpoint."""

    user_data = {
        "login": "login",
        "password": "password",
        "email": "email@email.com",
        "name": "name",
    }

    response = http_session.post(
        url=f"{sett.url}registration/",
        json=user_data,
    )

    assert response.status_code == HTTPStatus.OK

    postgres_data: dict = get_user_data(postgres_cur, "name")

    assert postgres_data.get("login") == user_data.get("login")
    assert postgres_data.get("email") == user_data.get("email")
    assert postgres_data.get("name") == user_data.get("name")
    assert postgres_data.get("password") != user_data.get("password")


def test_registration_unprocessable_entity(http_session: Session):
    """Test - for unprocessable entity error."""

    user_data = {
        "wrong_data": "i am wrong",
    }

    response = http_session.post(
        url=f"{sett.url}registration/",
        json=user_data,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
