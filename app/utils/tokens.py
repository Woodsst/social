import datetime
import time
import uuid
from typing import Dict, Any, Union

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError

from core.config import get_settings
from core.exceptions.jwt_exceptions import TokenValidityPeriodIsOver, TokenWrong

settings = get_settings()


def create_access_token(user_id: str) -> str:
    """Create access token with 1 hour lifetime."""
    delta = datetime.timedelta(hours=settings.jwt_access_lifetime_hour)
    payload = {
        "typ": "JWT",
        "sub": user_id,
        "exp": datetime.datetime.now() + delta,
        "jti": str(uuid.uuid4()),
        "iat": time.time(),
    }
    return jwt.encode(
        payload, settings.jwt_access_secret, algorithm=settings.jwt_algorithm
    )


def create_refresh_token(user_id: str) -> str:
    """Create refresh token with 2 weak lifetime."""
    delta = datetime.timedelta(days=settings.jwt_refresh_lifetime_day)
    payload = {
        "typ": "JWT",
        "sub": user_id,
        "exp": datetime.datetime.now() + delta,
        "jti": str(uuid.uuid4()),
        "iat": time.time(),
    }
    return jwt.encode(
        payload, settings.jwt_refresh_secret, algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode access token."""
    return jwt.decode(
        token, settings.jwt_access_secret, algorithms=settings.jwt_algorithm
    )


def decode_refresh_token(token: str) -> Dict[str, Any]:
    """Decode refresh token."""
    return jwt.decode(
        token, settings.jwt_refresh_secret, algorithms=settings.jwt_algorithm
    )


def generate_jwt_tokens(user_id: str) -> tuple:
    """Create access and refresh tokens."""
    access = create_access_token(user_id)
    refresh = create_refresh_token(user_id)
    return access, refresh


def update_access_token(refresh_token: str) -> Union[bool, tuple]:
    """Update access token by refresh token."""
    try:
        payload: dict = decode_refresh_token(refresh_token)
    except DecodeError:
        return False
    lifetime = payload.get("exp")
    if lifetime < time.time():  # type: ignore
        raise TokenValidityPeriodIsOver()
    return generate_jwt_tokens(payload.get("user_id"))  # type: ignore


def token_checkout(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> str:
    """Token checkout."""
    try:
        payload = decode_access_token(token.credentials)
    except DecodeError:
        raise TokenWrong()
    lifetime = payload.get("exp")
    if lifetime < time.time():  # type: ignore
        raise TokenValidityPeriodIsOver()
    return token.credentials
