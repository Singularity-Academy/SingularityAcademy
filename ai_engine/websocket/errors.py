"""
WebSocket error definitions for AI Engine.
"""

from typing import Optional, Dict, Any, ClassVar

class WebSocketError(Exception):
    """Base exception for WebSocket errors."""
    error_type: ClassVar[str] = "error"
    status_code: ClassVar[int] = 400
    
    def __init__(
        self, 
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.details = details or {}
        super().__init__(message)

class WebSocketAuthError(WebSocketError):
    """Authentication related WebSocket errors."""
    error_type = "auth_error"
    status_code = 401

class WebSocketValidationError(WebSocketError):
    """Validation related WebSocket errors."""
    error_type = "validation_error"
    status_code = 400

class WebSocketNotFoundError(WebSocketError):
    """Resource not found WebSocket errors."""
    error_type = "not_found_error"
    status_code = 404

class WebSocketConnectionError(WebSocketError):
    """Connection related WebSocket errors."""
    error_type = "connection_error"
    status_code = 500 