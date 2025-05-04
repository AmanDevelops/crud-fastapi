from fastapi import status


class AppException(Exception):
    def __init__(self, message: str = "Internal Server Error", status_code: int = 500):
        self.message = message
        self.status_code = status_code

class InvalidCredentialsException(AppException):
    def __init__(self, message: str = "Invalid username or password"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class NotFoundException(AppException):
    def __init__(self, message: str = "Review Not Found"):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)

class MissingDataException(AppException):
    def __init__(self, message = "Title and description are required", status_code = status.HTTP_400_BAD_REQUEST):
        super().__init__(message, status_code)