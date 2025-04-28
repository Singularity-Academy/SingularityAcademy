from sanic import Blueprint
from ujson import loads, dumps
from auth import AuthManager

bp = Blueprint("ws", url_prefix="/ws")

bp.ctx.auth = AuthManager.from_env()

@bp.websocket("/")
async def ws(request, ws):
    """
    Handles a websocket connection.
    This connection handles video and audio stream from the frontend.
    Authentication happens right after accepting.
    # Demo message
    {
        "type": "auth",
        "token": "1234567890"
    }
    # Response message
    {
        "status": "success",
        "health": "ok"
    }

    After auth, the frontend starts streaming video and audio at a rate of 1 req/sec.
    Currently we don't do anything with the video and audio stream.

    # Demo stream
    {
        "type": "stream",
        "data": {
            "video": "base64_encoded_video_data",
            "audio": "base64_encoded_audio_data"
        }
    }
    """
    data = await ws.recv()
    data = loads(data)
    if data["type"] == "auth":
        token = data["token"]
        try:
            user_id = bp.ctx.auth.decode_token(token)["ID"]
        except ValueError as e:
            await ws.send(dumps({
                "status": "error",
                "message": str(e)
            }))
            return
        else:
            await ws.send(dumps({
                "status": "success",
                "health": "ok"
            }))
    else:
        await ws.send(dumps({
            "status": "error",
            "message": "Invalid message type"
        }))
        return
    # demo code
    while True:
        data = await ws.recv()
        print(data)
        await ws.send(f"Received: {data}")
