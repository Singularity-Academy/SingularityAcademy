"""
Main application module for AI Engine.
"""

import threading
from sanic import Sanic, json, Blueprint, Request, Websocket
from sanic.response import json as json_response
from sanic.exceptions import NotFound, ServerError
from loguru import logger
from tortoise.exceptions import DoesNotExist
from tortoise.contrib.sanic import register_tortoise
from .db import init_db, User, PrincipalChatHistory
from .ai import Chat
from .websocket import bp as ws_bp
from .websocket.errors import WebSocketError
from .websocket.utils import send_ws_error, handle_ws_connection_error
from .auth import init_auth, authentication_middleware
from .courses import bp as courses_bp
from typing import Optional


logger.info("Starting AI Engine application")

app = Sanic("AIEngine")

# Initialize authentication first (attaches AuthManager to app.ctx.auth)
init_auth(app)

# Initialize database (loads config and registers Tortoise)
init_db(app)

# Create a main blueprint for HTTP routes that need authentication
# This keeps WebSocket routes separate
main_bp = Blueprint("main_http", url_prefix="/api")
main_bp.middleware("request")(authentication_middleware)

@app.listener('after_server_start')
async def notify_server_started(app, loop):
    """Notify when server is ready."""
    logger.info('Server started successfully!')

@app.route("/health")
async def health_check(request):
    """Health check endpoint."""
    return json_response({"status": "healthy"})

@main_bp.route("/ai/health/")
async def ai_health_auth_check(request):
    if not request.ctx.user_id:
        return json_response({"error": "Authentication required for AI health check"}, status=401)
    return json_response({"health": "ok", "user_id": request.ctx.user_id, "message": "AI components are healthy"})

# Register blueprints
app.blueprint(main_bp)
app.blueprint(ws_bp)  # WebSocket routes are now only registered through the blueprint
app.blueprint(courses_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, access_log=True)