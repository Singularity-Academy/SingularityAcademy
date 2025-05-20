import uuid
from sanic import Blueprint
from sanic.exceptions import WebsocketClosed

from ai_engine.apps.auth.utils import handle_ws_login
from ai_engine.logging import logger
from .stream_handlers import SimpleStreamHandler

bp = Blueprint("dean", url_prefix="/dean")

bp.ctx.stream_handler = SimpleStreamHandler()

@bp.websocket("/ws")
async def stream(request, ws):
    session_id = str(uuid.uuid4())[:8]
    remote = request.remote_addr or request.ip
    logger.info(f"New WebSocket connection from {remote} (session: {session_id})")
    try:
        await handle_ws_login(request, ws, session_id)

        # TODO: Handle streaming packets
        while True:
            data = await ws.recv()
            logger.info(f"Received data: {data}")
    except WebsocketClosed:
        logger.info(f"WebSocket closed (session: {session_id})")
        return
    except Exception as e:
        logger.error(f"Error handling WebSocket connection: {e}")
        await ws.close(code=1008)
        return
