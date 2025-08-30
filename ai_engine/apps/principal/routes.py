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

from ai_engine.apps.auth.utils import handle_ws_login

from ..auth import login_required
from ..ai.llm import LLM
from .chat import PrincipalChat
from .models import PrincipalChatHistory
from ..auth.models import User
from .utils import handle_course_req, send_ws_error, handle_user_message
from .ai_tools import CreateCourseTool, GetCourseTool, ListCoursesTool, UpdateCourseTool, DeleteCourseTool

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
        user = await handle_ws_login(request, ws, session_id)
        if not user:
            logger.info(f"WebSocket authentication unsuccessful (session: {session_id})")
            return
        
        # Get or create chat instance
        chat = await PrincipalChat.get_by_user(user.id)
        if not chat:
            await send_ws_error(ws, "Failed to initialize chat", 4004)
            return
        
        # Set up course management tools with user authentication (once per session)
        tools = [
            CreateCourseTool(user_id=user.id),
            GetCourseTool(user_id=user.id),
            ListCoursesTool(user_id=user.id),
            UpdateCourseTool(user_id=user.id),
            DeleteCourseTool(user_id=user.id),
        ]
        
        # Configure LLM with tools using the proper add_tool method (once per session)
        for tool in tools:
            llm.add_tool(tool)
        logger.info(f"[{session_id}] LLM configured with {len(tools)} tools for user {user.id}")

        # Send chat history
        try:
            # Convert messages to client format
            history_messages = []
            for msg in chat.history.messages[-10:]:
                logger.warning(f"History message: {msg}")

                if msg["role"] == "system":
                    continue
                
                history_messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                    "timestamp": msg["timestamp"],
                    "courses": msg["courses"]
                })
                logger.info(f"History message: {history_messages[-1]}")

                
            # Send only last 10 messages
            await ws.send(json.dumps({
                "type": "history_messages",
                "messages": history_messages
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

            # Process the message with all required arguments
            if data["type"] == "message":
                await handle_user_message(ws, chat, llm, data["content"], session_id)

            elif data["type"] == "message-reset":
                try:
                    await chat.reset()
                except Exception as e:
                    logger.error(f"Error resetting chat history: {e}")
                    await send_ws_error(ws, "Error resetting chat history", 400)
                    continue
                else:
                    await ws.send(json.dumps({
                        "type": "message-reset-success",
                        "message": "Chat history reset"
                    }))

            elif data["type"] == "course":
                await handle_course_req(ws, data["content"], session_id, llm)

            else:
                logger.info(f"[{session_id}] Unexpected message type: {data.get('type')}")
                await send_ws_error(ws, f"Unexpected message type: {data.get('type')}", 400)
                continue


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