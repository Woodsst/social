import datetime
import time
import uuid

import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import DecodeError

from core.config import get_settings
from core.exceptions.jwt_exceptions import TokenValidityPeriodIsOver, TokenWrong

settings = get_settings()


def create_access_token(user_id: str):
    """Create access token with 1 hour lifetime."""
    payload = {
        "typ": "JWT",
        "sub": user_id,
        "exp": datetime.datetime.now()
        + datetime.timedelta(hours=settings.jwt_access_lifetime),
        "jti": str(uuid.uuid4()),
        "iat": time.time(),
    }
    return jwt.encode(
        payload, settings.jwt_access_secret, algorithm=settings.jwt_algorithm
    )


def create_refresh_token(user_id: str):
    """Create refresh token with 2 weak lifetime."""
    payload = {
        "typ": "JWT",
        "sub": user_id,
        "exp": datetime.datetime.now()
        + datetime.timedelta(days=settings.jwt_refresh_lifetime),
        "jti": str(uuid.uuid4()),
        "iat": time.time(),
    }
    return jwt.encode(
        payload, settings.jwt_refresh_secret, algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str):
    """Decode access token."""
    return jwt.decode(
        token, settings.jwt_access_secret, algorithms=settings.jwt_algorithm
    )


def decode_refresh_token(token: str):
    """Decode refresh token."""
    return jwt.decode(
        token, settings.jwt_refresh_secret, algorithms=settings.jwt_algorithm
    )


def generate_jwt_tokens(user_id: str) -> tuple:
    """Create access and refresh tokens."""
    access = create_access_token(user_id)
    refresh = create_refresh_token(user_id)
    return access, refresh


def update_access_token(refresh_token):
    """Update access token by refresh token."""
    try:
        payload = decode_refresh_token(refresh_token)
    except DecodeError:
        return False
    lifetime = payload.get("exp")
    if lifetime < time.time():
        raise TokenValidityPeriodIsOver()
    return generate_jwt_tokens(payload.get("user_id"))


def token_checkout(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """Token checkout."""
    try:
        payload = decode_access_token(token.credentials)
    except DecodeError:
        raise TokenWrong()
    lifetime = payload.get("exp")
    if lifetime < time.time():
        raise TokenValidityPeriodIsOver()
    return token.credentials
