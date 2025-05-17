"""
Chat WebSocket endpoint for AI Engine.
"""

import ujson as json
import uuid
from loguru import logger
from sanic import Request, Websocket
from tortoise.exceptions import DoesNotExist
from tortoise.expressions import Q

from ..ai import Chat
from ..db import User, PrincipalChatHistory
from .errors import WebSocketError
from .utils import handle_ws_connection_error, send_ws_response, send_ws_error

async def process_message(ws: Websocket, chat: Chat, content: str, session_id: str) -> None:
    """
    Process a message from a WebSocket client.
    
    Args:
        ws: WebSocket connection
        chat: Chat instance to use
        content: Message content
        session_id: WebSocket session ID for logging
    """
    try:
        logger.info(f"[{session_id}] Processing message")
        
        # Stream the response - no longer yields chunks, now handled internally with websocket
        await chat.stream_message(content, websocket=ws)
        
    except ConnectionError as e:
        # Handle WebSocket connection errors gracefully without traceback
        logger.info(f"[{session_id}] WebSocket closed during streaming: {str(e)}")
    except Exception as e:
        logger.error(f"[{session_id}] Error streaming message: {str(e)}")
        import traceback
        traceback.print_exc()
        # Try to send error if connection is still open
        try:
            await send_ws_error(ws, f"Error processing message: {str(e)}", 500)
        except:
            # Connection likely closed, no need to report this error
            pass

async def chat_stream(request: Request, ws: Websocket):
    """
    WebSocket endpoint for streaming chat responses.
    
    Handles authentication and processes chat messages.
    
    Args:
        request: The request object
        ws: The WebSocket connection
    """
    client_ip = request.remote_addr or request.ip
    session_id = str(uuid.uuid4())[:8]  # Use first 8 characters for brevity
    
    try:
        # Wait for authentication message
        auth_message = await ws.recv()
        try:
            auth_data = json.loads(auth_message)
        except json.JSONDecodeError:
            await ws.send(json.dumps({
                "type": "error",
                "error": "Invalid authentication message format",
                "error_code": "INVALID_AUTH_FORMAT",
                "status_code": 400
            }))
            await ws.close(code=1008)
            return
            
        if not isinstance(auth_data, dict) or "token" not in auth_data:
            await ws.send(json.dumps({
                "type": "error",
                "error": "Authentication message must contain 'token' field",
                "error_code": "INVALID_AUTH_FORMAT",
                "status_code": 400
            }))
            await ws.close(code=1008)
            return
            
        # Verify token
        auth_manager = request.app.ctx.auth
        claims = auth_manager.decode_token(auth_data["token"])
        if not claims:
            await ws.send(json.dumps({
                "type": "error",
                "error": "Invalid or expired token",
                "error_code": "INVALID_TOKEN",
                "status_code": 401
            }))
            await ws.close(code=1008)
            return
            
        # Set user context
        user_id = claims.get("ID")
        if not user_id:
            await ws.send(json.dumps({
                "type": "error",
                "error": "Invalid token claims",
                "error_code": "INVALID_TOKEN_CLAIMS",
                "status_code": 401
            }))
            await ws.close(code=1008)
            return
            
        # Verify user exists in database
        try:
            user = await User.get(id=user_id)
        except DoesNotExist:
            await ws.send(json.dumps({
                "type": "error",
                "error": "User not found in database",
                "error_code": "USER_NOT_FOUND",
                "status_code": 404
            }))
            await ws.close(code=1008)
            return
        
        # Get or create chat history for the user
        try:
            chat_history = await PrincipalChatHistory.get_or_create(user=user)
        except Exception as e:
            logger.error(f"[{session_id}] Error getting/creating chat history for user {user_id}: {e}")
            await send_ws_error(ws, "Failed to initialize chat", 500)
            return
        
        chat_history = chat_history[0]
        
        # Create a single Chat instance to use for the entire session
        chat = Chat(user, chat_history.id)
        
        # Send authentication success message
        await ws.send(json.dumps({
            "type": "auth_success",
            "message": "Authentication successful",
            "user_id": user_id
        }))
        logger.info(f"[{session_id}] Authorized: User {user_id} from {client_ip}")
        
        # Fetch and send the last 10 messages from chat history (if any exist)
        try:
            # Get last 10 messages, skipping system messages
            history_messages = await chat.get_history_messages()
            user_messages = [msg for msg in history_messages if msg.get('role') != 'system']
            recent_messages = user_messages[-10:] if len(user_messages) > 0 else []
            
            if recent_messages:
                logger.info(f"[{session_id}] Sending {len(recent_messages)} recent messages to client")
                await ws.send(json.dumps({
                    "type": "history_messages",
                    "messages": recent_messages
                }))
        except Exception as e:
            logger.error(f"[{session_id}] Error sending chat history: {e}")
            # Non-critical error, continue with connection
        
        # Main message handling loop
        try:
            async for message in ws:
                try:
                    data = json.loads(message)
                    if not isinstance(data, dict):
                        logger.info(f"[{session_id}] Invalid message format: {message[:50]}...")
                        await send_ws_error(ws, "Invalid message format", 400)
                        continue
                        
                    if "type" not in data:
                        logger.info(f"[{session_id}] Missing message type")
                        await send_ws_error(ws, "Message must include 'type' field", 400)
                        continue
                        
                    if data["type"] != "message":
                        logger.info(f"[{session_id}] Unexpected message type: {data.get('type')}")
                        await send_ws_error(ws, f"Unexpected message type: {data.get('type')}", 400)
                        continue
                        
                    if "content" not in data or not data["content"].strip():
                        logger.info(f"[{session_id}] Empty message content")
                        await send_ws_error(ws, "Message content cannot be empty", 400)
                        continue

                    # Process the message using the existing chat instance
                    logger.info(f"[{session_id}] Processing message")
                    await process_message(ws, chat, data["content"], session_id)
                    
                except json.JSONDecodeError:
                    logger.info(f"[{session_id}] Invalid JSON message format")
                    await send_ws_error(ws, "Invalid message format", 400)
                except Exception as e:
                    logger.error(f"[{session_id}] Error processing message: {e}")
                    await send_ws_error(ws, "Internal server error", 500)
                    
        except ConnectionError as e:
            # Handle WebSocket connection errors gracefully without traceback
            logger.info(f"[{session_id}] WebSocket connection closed: {str(e)}")
        except Exception as e:
            logger.error(f"[{session_id}] WebSocket error: {e}")
            import traceback
            traceback.print_exc()
            
    except ConnectionError as e:
        # Handle WebSocket connection errors gracefully without traceback
        logger.info(f"[{session_id}] WebSocket connection error (likely code 1006): {str(e)}")
    except Exception as e:
        logger.error(f"[{session_id}] WebSocket connection error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'user_id' in locals():
            logger.info(f"[{session_id}] WebSocket disconnected: User {user_id} from {client_ip}") 