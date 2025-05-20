from sanic.exceptions import WebsocketClosed
from tortoise.exceptions import DoesNotExist
import ujson as json

from .models import User
from ai_engine.logging import logger

async def handle_ws_login(request, ws, session_id):
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

    return user
    