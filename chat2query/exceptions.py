"""Chat2Query SDK Exceptions"""

from typing import Optional


class Chat2QueryError(Exception):
    """Base exception for Chat2Query SDK"""


class AuthenticationError(Chat2QueryError):
    """Raised when authentication fails"""


class APIError(Chat2QueryError):
    """Raised when API returns an error"""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class NotFoundError(APIError):
    """Raised when a resource is not found"""


class ValidationError(Chat2QueryError):
    """Raised when request validation fails"""
