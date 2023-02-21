from http import HTTPStatus

from requests import Session

from config import get_settings

sett = get_settings()


def registration(http_session: Session, user_data: dict) -> None:
    """Registration request."""

    response = http_session.post(
        url=f"{sett.url}registration/",
        json=user_data,
    )

    assert response.status_code == HTTPStatus.OK


def login(http_session: Session, user_data: dict) -> dict:
    """Login request."""

    response = http_session.post(
        url=f"{sett.url}login/",
        json=user_data,
    )

    assert response.status_code == HTTPStatus.OK

    return response.json()
