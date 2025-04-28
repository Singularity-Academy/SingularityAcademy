from sanic import Sanic
from sanic.response import json
from .config import get_config
from ai_engine.ws import bp as video_bp

config = get_config()

app = Sanic("AI-Engine")

app.blueprint(video_bp)

@app.route("/health")
async def health(request):
    return json({"status": "ok"})




