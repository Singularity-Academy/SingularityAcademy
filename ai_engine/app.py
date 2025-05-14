from sanic import Sanic, json, Blueprint
from ai_engine.db import init_db, User
from sanic.response import json as json_response
import logging
from .ws import bp as ws_bp
from .auth import init_auth, authentication_middleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = Sanic("AIEngine")

# Initialize authentication first (attaches AuthManager to app.ctx.auth)
init_auth(app)

# Initialize database (can use app.ctx.auth if needed, though not directly here)
init_db(app)

# Create a main blueprint for HTTP routes that need authentication
# This keeps WebSocket routes separate
main_bp = Blueprint("main_http", url_prefix="/api")
main_bp.middleware("request")(authentication_middleware)

@app.listener('after_server_start')
async def notify_server_started(app, loop):
    logger.info('Server started successfully!')

@app.route("/health")
async def health_check(request):
    return json_response({"status": "healthy"})

@main_bp.route("/ai/health/")
async def ai_health_auth_check(request):
    if not request.ctx.user_id:
        return json_response({"error": "Authentication required for AI health check"}, status=401)
    return json_response({"health": "ok", "user_id": request.ctx.user_id, "message": "AI components are healthy"})

app.blueprint(main_bp)
app.blueprint(ws_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, access_log=True)