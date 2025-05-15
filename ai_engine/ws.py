from sanic import Sanic
from sanic.blueprints import Blueprint
from ujson import loads, dumps
from .exceptions import AuthError
from .auth import AuthManager
from .ai import Chat
from .db import User
import base64
import os
import time
import logging
from typing import Dict, Any, Optional, Tuple, Union

# Import helpers and constants
from .ws_helpers import (
    # Constants
    MSG_TYPE_AUTH, MSG_TYPE_AUTH_RESPONSE, MSG_TYPE_MESSAGE, 
    MSG_TYPE_MESSAGE_RESPONSE, MSG_TYPE_ERROR, MSG_TYPE_ACK,
    # Helper functions
    handle_authentication, send_error_response,
    process_chat_message, save_video_frame, process_stream_packet
)

# Set up logging
logger = logging.getLogger(__name__)

# Create frames directory if it doesn't exist
os.makedirs("frames", exist_ok=True)

bp = Blueprint("ws", url_prefix="/ai/ws")

@bp.websocket("/principal")
async def principal(request, ws):
    """
    Handles a single Principal AI chat connection.
    Lifecycle:
     - accepts and waits for auth msg
     - check auth data and verifies it
     - returns auth_ok msg
     - starts receiving chat messages and processes them through LLM

    Message format for frontend -> backend:
    {
        "type": "auth",
        "token": "jwt_token_here"
    }
    
    OR
    
    {
        "type": "message",
        "content": "User's message here"
    }

    Message format for backend -> frontend:
    {
        "type": "auth_response",
        "status": "success",
        "user_id": "1234"
    }
    
    OR
    
    {
        "type": "message_response",
        "content": {
            "text": "Response from LLM",
            "calls": [] # Any function calls (empty for now)
        },
        "message_id": "prinmsg-uuid..."
    }
    """
    logger.info("Principal chat WebSocket connection established")
    chat_session = None
    user_id = None
    
    try:
        # Authenticate user and send success response in one step
        claims, user_id = await handle_authentication(ws, request)
        
        # Fetch user from database
        try:
            user = await User.get(id=claims["ID"])
            logger.info(f"Found user: {user.username} (ID: {user_id})")
        except Exception as e:
            logger.error(f"Failed to retrieve user {user_id}: {e}")
            raise AuthError(f"User not found: {e}")
        
        # Create chat session
        chat_session = Chat(user=user)
        
        # Start receiving chat messages
        logger.info(f"Starting to receive chat messages for user {user_id}")
        while True:
            try:
                message = await ws.recv()
                message_data = loads(message)
                await process_chat_message(ws, chat_session, message_data, user_id)
            except AuthError as e:
                logger.error(f"Auth error during message processing: {e}")
                await send_error_response(ws, MSG_TYPE_ERROR, f"Authentication error: {str(e)}")
                break
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                await send_error_response(ws, MSG_TYPE_ERROR, f"Error processing your message: {str(e)}")
    
    except AuthError as e:
        logger.error(f"Authentication error: {e}")
        await send_error_response(ws, MSG_TYPE_AUTH_RESPONSE, str(e))
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await send_error_response(ws, MSG_TYPE_ERROR, f"Server error: {str(e)}")
    finally:
        # Ensure connection is closed
        logger.info(f"Principal chat WebSocket connection closed for user {user_id}")
        await ws.close()

@bp.websocket("/stream")
async def stream_handler(request, ws):
    """
    Handles a single WebSocket Video & Audio streaming connection.
    Lifecycle:
     - accepts and waits for auth msg
     - check auth data and verifies it
     - returns auth_ok msg
     - starts receiving video & audio chunks
    Frontend -> backend auth msg:
    {
        "type": "auth",
        "token": "1234567890"
    }
    Backend -> frontend auth_ok msg:
    {
        "type": "auth_response",
        "status": "success",
        "user_id": "1234567890"
    }
    Stream data:
    {
        "packet_id": 123,
        "time": 1234567890, # unix timestamp
        "video": "base64_encoded_video_data",
        "audio": "base64_encoded_audio_data"
    }
    """
    logger.info("WebSocket stream connection established")
    user_id = None
    
    try:
        # Authenticate user and send success response in one step
        claims, user_id = await handle_authentication(ws, request)
        
        # Create a unique session folder using timestamp
        session_id = int(time.time())
        session_dir = f"frames/session_{session_id}"
        os.makedirs(session_dir, exist_ok=True)
        logger.info(f"Created session directory: {session_dir}")
        
        # Start receiving video & audio chunks
        logger.info("Starting to receive video/audio data")
        while True:
            chunk = await ws.recv()
            try:
                chunk_data = loads(chunk)
                await process_stream_packet(ws, chunk_data, session_dir)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                logger.debug(f"Message content (first 100 chars): {str(chunk)[:100]}")
        
    except AuthError as e:
        logger.error(f"Authentication error: {e}")
        await send_error_response(ws, MSG_TYPE_AUTH_RESPONSE, str(e))
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        raise
    finally:
        # Ensure connection is closed
        logger.info(f"WebSocket stream connection closed for user {user_id}")
        await ws.close()