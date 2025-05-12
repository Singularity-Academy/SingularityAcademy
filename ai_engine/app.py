from sanic import Sanic, json
from ai_engine.db import init_db, User
from sanic.response import json as json_response
import logging
from .ws import bp as ws_bp
from .auth import AuthManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = Sanic("AIEngine")

# Initialize database
init_db(app)

app.ctx.auth = AuthManager.from_env()

app.blueprint(ws_bp)

@app.listener('after_server_start')
async def notify_server_started(app, loop):
    logger.info('Server started successfully!')

@app.route("/health")
async def health_check(request):
    return json_response({"status": "healthy"})

@app.route("/ai/health/")
async def health(request):
    return json({"health": "ok"})