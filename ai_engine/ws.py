from sanic import Blueprint

bp = Blueprint("video", url_prefix="/ws")

@bp.websocket("/")
async def ws(request, ws):
    # demo code
    while True:
        data = await ws.recv()
        print(data)
        await ws.send(f"Received: {data}")
