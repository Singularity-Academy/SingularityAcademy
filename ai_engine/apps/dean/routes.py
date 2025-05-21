import uuid
from sanic import Blueprint
from sanic.exceptions import WebsocketClosed
import ujson as json

from ai_engine.apps.auth.utils import handle_ws_login
from ai_engine.logging import logger
from .stream_handlers import StreamHandler

bp = Blueprint("dean", url_prefix="/dean")

@bp.websocket("/ws")
async def stream(request, ws):
    session_id = str(uuid.uuid4())[:8]
    stream_handler = None
    remote = request.remote_addr or request.ip
    logger.info(f"New WebSocket connection from {remote} (session: {session_id})")
    try:
        user = await handle_ws_login(request, ws, session_id)
        if not user:
            logger.info(f"WebSocket authentication unsuccessful (session: {session_id})")
            return

        # Initialize stream handler
        stream_handler = StreamHandler(user_id=user.id)
        stream_handler.start_recording()
        logger.info(f"Started recording for user {user.id}")

        while True:
            data = await ws.recv()
            data = json.loads(data)

            if data.get('video'):
                await stream_handler.save_video_frame(data['video'])
            if data.get('audio'):
                await stream_handler.save_audio_frame(data['audio'])

            logger.trace(f"Received data frames: {'audio' if data.get('audio') else ''} {'video' if data.get('video') else ''}")

    except WebsocketClosed:
        logger.info(f"WebSocket closed (session: {session_id})")
        return
    except Exception as e:
        logger.error(f"Error handling WebSocket connection: {e}")
        import traceback
        traceback.print_exc()
        await ws.close(code=1008)
        return
    finally:
        if stream_handler:
            await stream_handler.stop_recording()
