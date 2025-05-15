from ujson import loads, dumps
from .exceptions import AuthError
from .ai import Chat
from .db import User
import base64
import logging
from typing import Dict, Any, Optional, Tuple, Union

logger = logging.getLogger(__name__)

# Message type constants
MSG_TYPE_AUTH = "auth"
MSG_TYPE_AUTH_RESPONSE = "auth_response"
MSG_TYPE_MESSAGE = "message"
MSG_TYPE_MESSAGE_RESPONSE = "message_response"
MSG_TYPE_ERROR = "error"
MSG_TYPE_ACK = "ack"

async def authenticate_websocket(ws, request) -> Tuple[Dict[str, Any], str]:
    """
    Authenticate a websocket connection using JWT token.
    
    Args:
        ws: The websocket connection
        request: The Sanic request object
        
    Returns:
        Tuple containing (user claims dict, user_id string)
        
    Raises:
        AuthError: If authentication fails
    """
    # Get auth manager from request context
    auth_manager = request.app.ctx.auth
    
    # Wait for authentication message
    logger.info("Waiting for auth message...")
    auth_message = await ws.recv()
    auth_data = loads(auth_message)
    
    if auth_data.get("type") != MSG_TYPE_AUTH or not auth_data.get("token"):
        logger.warning("Invalid auth data format")
        raise AuthError("Invalid message type or missing token")
    
    # Verify auth token
    token = auth_data.get("token")
    logger.info(f"Verifying token: {token[:10]}...")
    
    if not auth_manager.verify_token(token):
        logger.warning("Token verification failed")
        raise AuthError("Invalid token")
    
    # Get user ID from token
    claims = auth_manager.decode_token(token)
    if not claims or "ID" not in claims:
        logger.warning("Token valid but missing ID claim")
        raise AuthError("Invalid token structure")
    
    user_id = claims["ID"]
    logger.info(f"Auth successful for user {user_id}")
    
    return claims, str(user_id)

async def send_auth_success_response(ws, user_id: str) -> None:
    """Send authentication success response to client."""
    await ws.send(dumps({
        "type": MSG_TYPE_AUTH_RESPONSE,
        "status": "success",
        "user_id": user_id
    }))

async def handle_authentication(ws, request) -> Tuple[Dict[str, Any], str]:
    """
    Complete authentication flow including response.
    
    This function combines authenticate_websocket and send_auth_success_response
    into a single operation for convenience.
    
    Args:
        ws: The websocket connection
        request: The Sanic request object
        
    Returns:
        Tuple containing (user claims dict, user_id string)
        
    Raises:
        AuthError: If authentication fails
    """
    claims, user_id = await authenticate_websocket(ws, request)
    await send_auth_success_response(ws, user_id)
    return claims, user_id

async def send_error_response(ws, error_type: str, message: str) -> None:
    """Send an error response to client."""
    await ws.send(dumps({
        "type": error_type,
        "status": "error",
        "message": message
    }))

async def process_chat_message(ws, chat_session: Chat, message_data: Dict[str, Any], user_id: str) -> None:
    """
    Process a chat message from the user and send response.
    
    Args:
        ws: The websocket connection
        chat_session: The Chat instance for this user
        message_data: The message data from the client
        user_id: The user's ID
    """
    if message_data.get("type") != MSG_TYPE_MESSAGE:
        logger.warning(f"Unexpected message type: {message_data.get('type')}")
        await send_error_response(ws, MSG_TYPE_ERROR, "Unexpected message type. Expected 'message'.")
        return
    
    user_content = message_data.get("content")
    if not user_content:
        logger.warning("Empty message content received")
        await send_error_response(ws, MSG_TYPE_ERROR, "Message content cannot be empty.")
        return
    
    logger.info(f"Received message from user {user_id}: {user_content[:50]}...")
    
    # Send to LLM using our Chat class
    response = await chat_session.send_message(user_content)
    
    # Check for errors
    if response.get("error"):
        logger.error(f"Error processing message: {response.get('error')}")
        await send_error_response(ws, MSG_TYPE_ERROR, f"Error processing your message: {response.get('error')}")
        return
    
    # Format and send response back to frontend
    logger.info(f"Sending LLM response back to user {user_id}")
    await ws.send(dumps({
        "type": MSG_TYPE_MESSAGE_RESPONSE,
        "content": response.get("content", {}),
        "message_id": response.get("message_id", "")
    }))

async def save_video_frame(session_dir: str, packet_id: int, base64_data: str) -> str:
    """
    Save a video frame from base64 data to file.
    
    Args:
        session_dir: Directory to save the frame in
        packet_id: ID of the frame packet
        base64_data: Base64-encoded image data
        
    Returns:
        Path to the saved file
    """
    # Decode the base64 data
    image_data = base64.b64decode(base64_data)
    
    # Save to file
    file_path = f"{session_dir}/frame_{packet_id}.jpg"
    with open(file_path, "wb") as f:
        f.write(image_data)
    
    logger.info(f"Saved frame #{packet_id} to {file_path}")
    return file_path

async def process_stream_packet(ws, chunk_data: Dict[str, Any], session_dir: str) -> None:
    """Process a video/audio stream packet."""
    # Process video frames
    if chunk_data.get("video") is not None:
        packet_id = chunk_data.get('packet_id')
        logger.info(f"Received video packet #{packet_id} at time {chunk_data.get('time')}")
        
        try:
            # Get the base64 encoded frame
            base64_data = chunk_data.get("video")
            file_path = await save_video_frame(session_dir, packet_id, base64_data)
        except Exception as e:
            logger.error(f"Error saving frame #{packet_id}: {e}")
        
        # Send acknowledgment if needed
        await ws.send(dumps({
            "type": MSG_TYPE_ACK,
            "packet_id": packet_id,
            "message": f"Frame {packet_id} received and saved"
        }))
    
    # Process audio frames
    if chunk_data.get("audio") is not None:
        packet_id = chunk_data.get('packet_id')
        logger.info(f"Received audio packet #{packet_id} at time {chunk_data.get('time')}")
        
        # Audio processing would go here 