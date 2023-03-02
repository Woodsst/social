from http import HTTPStatus

from requests import Session, Response

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


def get_user_data(http_session: Session, access_token: str) -> dict:
    """Request to getting user data."""

    response = http_session.get(
        f"{sett.url}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == HTTPStatus.OK

    return response.json()


def add_post(http_session: Session, access_token: str, post_data: dict) -> Response:
    """Request to add new post."""

    response = http_session.post(
        url=f"{sett.url}post/add",
        headers={"Authorization": f"Bearer {access_token}"},
        json=post_data,
    )

    assert response.status_code == HTTPStatus.OK

    return response
