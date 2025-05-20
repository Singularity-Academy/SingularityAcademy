"""
WebSocket routes for the principal application.

This module handles WebSocket connections for chat functionality,
including authentication, message streaming, and chat history.
"""

import ujson as json
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from loguru import logger
from sanic import Blueprint, Request, Websocket, json as sanic_json
from sanic.exceptions import WebsocketClosed
from tortoise.exceptions import DoesNotExist
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from ..auth import login_required
from ..ai.llm import LLM
from .chat import PrincipalChat
from .models import PrincipalChatHistory
from ..auth.models import User
from .utils import send_ws_error, process_message

bp = Blueprint("principal", url_prefix="/principal-ai")

@bp.websocket("/ws/chat")
async def websocket(request: Request, ws: Websocket):
    """
    WebSocket endpoint for streaming chat responses.
    
    Handles authentication and processes chat messages.
    
    Args:
        request: The request object
        ws: The WebSocket connection
    """
    client_ip = request.remote_addr or request.ip
    session_id = str(uuid.uuid4())[:8]
    logger.info(f"New WebSocket connection from {client_ip} (session: {session_id})")
    
    # Initialize LLM
    llm = LLM()
    
    try:
        # Wait for authentication message
        try:
            auth_message = await ws.recv()
        except WebsocketClosed:
            logger.info(f"WebSocket closed before authentication (session: {session_id})")
            return
            
        try:
            auth_data = json.loads(auth_message)
            if not isinstance(auth_data, dict) or "token" not in auth_data:
                await ws.send(json.dumps({
                    "type": "error",
                    "error": "Authentication message must contain 'token' field",
                    "error_code": "INVALID_AUTH_FORMAT",
                    "status_code": 400
                }))
                await ws.close(code=1008)
                return
        except json.JSONDecodeError:
            await ws.send(json.dumps({
                "type": "error",
                "error": "Invalid authentication message format",
                "error_code": "INVALID_AUTH_FORMAT",
                "status_code": 400
            }))
            await ws.close(code=1008)
            return
            
        # Verify token using auth manager
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
            
        # Get user ID from claims
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
            
        logger.info(f"User {user.email} authenticated (session: {session_id})")
        
        # Send authentication success message
        await ws.send(json.dumps({
            "type": "auth_success",
            "message": "Authentication successful",
            "user_id": user_id
        }))
        
        # Get or create chat instance
        chat = await PrincipalChat.get_by_user(user.id)
        if not chat:
            await send_ws_error(ws, "Failed to initialize chat", 4004)
            return
        
        # Send chat history
        try:
            # Convert messages to client format
            history_messages = []
            for msg in chat.langchain_messages:
                # Skip system messages
                if isinstance(msg, SystemMessage):
                    continue
                    
                # Convert to dict format
                history_messages.append({
                    "role": "user" if isinstance(msg, HumanMessage) else "assistant",
                    "content": msg.content,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
                
            # Send only last 10 messages
            await ws.send(json.dumps({
                "type": "history_messages",
                "messages": history_messages[-10:]
            }))
        except WebsocketClosed:
            logger.info(f"WebSocket closed while sending history (session: {session_id})")
            return
        except Exception as e:
            logger.error(f"Error sending chat history: {e}")
            try:
                await send_ws_error(ws, "Error sending chat history", 4007)
            except WebsocketClosed:
                logger.info(f"WebSocket closed while sending error (session: {session_id})")
            return
            
        # Process messages
        while True:
            message = await ws.recv()
            try:
                data = json.loads(message)
                            
            except json.JSONDecodeError:
                logger.info(f"[{session_id}] Invalid JSON message format")
                await send_ws_error(ws, "Invalid message format", 400)
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

            # Process the message with all required arguments
            await process_message(ws, chat, llm, data["content"], session_id)


    except WebsocketClosed:
        logger.info(f"WebSocket connection closed (session: {session_id})")
    except RuntimeError as e:
        logger.info(f"WebSocket unexpectedly closed (session: {session_id})")
    except Exception as e:
        logger.error(f"Unexpected error in WebSocket handler: {e}")
        try:
            await send_ws_error(ws, "Internal server error", 4006)
        except WebsocketClosed:
            logger.info(f"WebSocket closed while sending error (session: {session_id})")
    finally:
        logger.info(f"WebSocket connection ended (session: {session_id})")