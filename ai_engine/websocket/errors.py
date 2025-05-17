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