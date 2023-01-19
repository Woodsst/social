from http import HTTPStatus

from starlette.exceptions import HTTPException


class TokenValidityPeriodIsOver(HTTPException):
    """Exception for token lifetime is over."""

    def __init__(self, status_code=HTTPStatus.UNAUTHORIZED):
        super().__init__(status_code=status_code, detail="Token validity period is over")
        self.status_code = status_code


class TokenWrong(HTTPException):
    """Exception for wrong token format."""

    def __init__(self, status_code=HTTPStatus.CONFLICT):
        super().__init__(status_code=status_code, detail="Wrong token format")
        self.status_code = status_code
