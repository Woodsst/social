from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


class RegistrationStatus(str, Enum):
    """Registration statuses enumeration."""

    complete = "complete"
    user_exists = "user exists"


class RegistrationRequest(BaseModel):
    """Registration request model."""

    login: str
    password: str
    email: EmailStr


class RegistrationResponse(BaseModel):
    """Registration response model."""

    registration_status: RegistrationStatus


class LoginStatus(str, Enum):
    """Login statuses enumeration."""

    complete = "complete"
    wrong_password = "wrong password"
    user_not_exist = "user not exist"


class LoginRequest(BaseModel):
    """Login request model."""

    login: str
    password: str


class Tokens(BaseModel):

    access_token: Optional[str]
    refresh_token: Optional[str]


class LoginResponse(Tokens):
    """Login response model."""

    login_status: LoginStatus = LoginStatus.complete


class LoginWrong(BaseModel):
    """Wrong password response model."""

    login_status: LoginStatus = LoginStatus.wrong_password


class WrongToken(BaseModel):
    """Model for wrong token."""

    message: str = "Wrong token"
