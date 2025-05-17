"""
WebSocket module for AI Engine.
"""

from sanic import Blueprint
from .chat import chat_stream

# Create WebSocket blueprint for PrincipalAI
bp = Blueprint("principal_ai_ws", url_prefix="/principal-ai/ws")

# Register WebSocket routes
bp.add_websocket_route(chat_stream, "/chat")

__all__ = ["bp", "chat_stream"] 