from fastapi import status

class CommonException(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__()
        self.code = code
        self.message = message

class BadRequest(CommonException):
    def __init__(self, message: str) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, message)

class Forbidden(CommonException):
    def __init__(self, message: str) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, message)

class NotFound(CommonException):
    def __init__(self, message: str) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, message)

class InternalServerError(CommonException):
    def __init__(self, message: str) -> None:
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, message)
