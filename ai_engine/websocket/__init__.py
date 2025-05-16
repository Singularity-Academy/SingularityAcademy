"""
WebSocket module for AI Engine.
"""

from sanic import Blueprint
from .chat import chat_stream

# Create WebSocket blueprint
bp = Blueprint("websocket", url_prefix="/ws")

# Register WebSocket routes
bp.add_websocket_route(chat_stream, "/chat/<chat_id:int>")

__all__ = ["bp", "chat_stream"] 