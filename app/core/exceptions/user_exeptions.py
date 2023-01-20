from http import HTTPStatus

from starlette.exceptions import HTTPException


class UserNotFound(HTTPException):
    """Exception for "user not found" error."""

    def __init__(self, status_code=HTTPStatus.NOT_FOUND):
        super().__init__(status_code=status_code, detail="User not found")
        self.status_code = status_code
