from http import HTTPStatus

from starlette.exceptions import HTTPException


class PostNotFound(HTTPException):
    """Exception for "post not found" error."""

    def __init__(self, status_code: HTTPStatus = HTTPStatus.NOT_FOUND):
        super().__init__(status_code=status_code, detail="Post not found")
        self.status_code = status_code
