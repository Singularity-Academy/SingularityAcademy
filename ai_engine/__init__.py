from sanic import Sanic
from sanic.response import json

app = Sanic("AI-Engine")

@app.route("/health")
async def health(request):
    return json({"status": "ok"})


