from sanic import Blueprint

bp = Blueprint("dean", url_prefix="/dean")

@bp.websocket("/ws")
def stream(request, ws):
    pass