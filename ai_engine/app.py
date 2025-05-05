from sanic import Sanic
from sanic.response import json
from .ws import bp as ws_bp
from .auth import AuthManager

app = Sanic("AI_Engine")

app.ctx.auth = AuthManager.from_env()

app.blueprint(ws_bp)

@app.route("/ai/health/")
async def health(request):
    return json({"health": "ok"})
