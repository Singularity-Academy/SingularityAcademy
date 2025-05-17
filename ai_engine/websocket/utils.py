"""
WebSocket utility functions for AI Engine.
"""

from typing import Optional, Dict, Any
from datetime import datetime
import ujson as json
from loguru import logger
from sanic import Websocket


async def send_ws_error(
    ws: Websocket,
    message: str,
    error_type: str = "error",
    status_code: int = 500,
    details: Optional[Dict[str, Any]] = None,
    exception: Optional[Exception] = None
) -> None:
    """
    Send a standardized error response through WebSocket.
    
    Args:
        ws: WebSocket connection
        message: Error message
        error_type: Type of error
        status_code: HTTP status code
        details: Optional additional error details
        exception: Optional exception for logging
    """
    error_data = {
        "message": message,
        "error_type": error_type,
        "status_code": status_code,
        **(details or {})
    }
    
    if exception:
        logger.error(f"WebSocket error: {message}", exc_info=exception)
    else:
        logger.warning(f"WebSocket error: {message}")
        
    await send_ws_message(ws, error_data, error_type, "error")

async def send_ws_message(
    ws: Websocket,
    data: Dict[str, Any],
    message_type: str = "message",
    status: str = "success",
    error: Optional[Exception] = None
) -> None:
    """
    Send a standardized message through WebSocket.
    
    Args:
        ws: WebSocket connection
        data: Message data or error details
        message_type: Type of message
        status: Message status (success/error)
        error: Optional exception for logging
    """
    try:
        message = {
            "type": message_type,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            **({"data": data} if status == "success" else data)
        }
        
        if error:
            logger.error(f"WebSocket {message_type}: {data.get('message', '')}", exc_info=error)
        elif status == "error":
            logger.warning(f"WebSocket {message_type}: {data.get('message', '')}")
            
        await ws.send(json.dumps(message))
    except Exception as e:
        logger.error(f"Failed to send WebSocket message: {e}") 