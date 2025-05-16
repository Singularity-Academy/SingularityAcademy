"""
Exception classes for AI Engine.
"""

class AIEngineError(Exception):
    """Base exception class for AI Engine errors."""
    def __init__(self, message: str, error_type: str = "error", status_code: int = 500, details: dict = None):
        self.message = message
        self.error_type = error_type
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(AIEngineError):
    """Exception raised for validation errors."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=message,
            error_type="validation_error",
            status_code=400,
            details=details
        )

class NotFoundError(AIEngineError):
    """Exception raised when a resource is not found."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=message,
            error_type="not_found_error",
            status_code=404,
            details=details
        )

class AuthenticationError(AIEngineError):
    """Exception raised for authentication errors."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=message,
            error_type="auth_error",
            status_code=401,
            details=details
        )

class AuthorizationError(AIEngineError):
    """Exception raised for authorization errors."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=message,
            error_type="forbidden_error",
            status_code=403,
            details=details
        )

__all__ = [
    'AIEngineError',
    'ValidationError',
    'NotFoundError',
    'AuthenticationError',
    'AuthorizationError'
] 