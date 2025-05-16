"""
Chat WebSocket endpoint for AI Engine.
"""

import ujson as json
from loguru import logger
from sanic import Request, Websocket
from tortoise.exceptions import DoesNotExist

from ..ai import Chat
from ..db import User, PrincipalChatHistory
from .errors import WebSocketError
from .utils import handle_ws_connection_error

async def chat_stream(request: Request, ws: Websocket, chat_id: int):
    """
    WebSocket endpoint for streaming chat responses.
    """
    try:
        # Get user and chat history in one try block
        try:
            user = await User.get(username="testuser")  # TODO: Implement proper auth
            history = await PrincipalChatHistory.get(id=chat_id, user=user)
        except DoesNotExist as e:
            raise WebSocketError("User not found") if "User" in str(e) else WebSocketError("Chat not found")

        chat = Chat(user=user, chat_history_id=chat_id)
        
        while True:
            try:
                message = await ws.recv()
                if not message:
                    continue
                
                # Parse and validate message in one step
                try:
                    data = json.loads(message)
                    if not (user_message := data.get("message", "").strip()):
                        raise WebSocketError("Empty message")
                except json.JSONDecodeError:
                    raise WebSocketError("Invalid message format")
                
                # Stream response
                async for _ in chat.stream_message(
                    user_message, 
                    model_id=data.get("model_id"), 
                    websocket=ws
                ):
                    pass  # Chunks are sent via StreamingCallbackHandler
                    
            except WebSocketError as e:
                await handle_ws_connection_error(ws, e)
                if e.status_code >= 400:
                    break
            except Exception as e:
                logger.error(f"Stream error: {e}")
                await handle_ws_connection_error(ws, e)
                break
                
    except Exception as e:
        await handle_ws_connection_error(ws, e)
    finally:
        await ws.close() 