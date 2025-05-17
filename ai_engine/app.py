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
from .db import init_db, User, PrincipalChatHistory, load_db_config
from .ai import Chat
from .websocket import bp as ws_bp
from .websocket.errors import WebSocketError
from .websocket.utils import send_ws_error, handle_ws_connection_error
from .auth import init_auth, authentication_middleware
from .courses import bp as courses_bp
from typing import Optional
from sanic_cors import CORS
import sys

logger.info("Starting AI Engine application")

def log_routes(app: Sanic):
    """Log all registered routes in a readable format."""
    logger.info("Registered Routes:")
    logger.info("-" * 80)
    
    # Get all routes and sort them by path
    routes = sorted(
        [
            {
                "path": route.path,
                "methods": route.methods,
                "name": route.name,
                "handler": route.handler.__name__,
                "is_websocket": hasattr(route.handler, "websocket") and route.handler.websocket
            }
            for route in app.router.routes
        ],
        key=lambda x: x["path"]
    )
    
    # Log each route with proper formatting
    for route in routes:
        if route["is_websocket"]:
            methods = "WebSocket"
        else:
            methods = ", ".join(route["methods"])
        logger.info(f"{methods:15} {route['path']:40} -> {route['handler']}")
    
    logger.info("-" * 80)

app = Sanic("ai_engine")

# Configure CORS
"""
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:1298", "http://127.0.0.1:1298"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["*"],
        "expose_headers": ["*"],
        "supports_credentials": True
    }
})
"""

# Development mode configuration
app.config.update({
    "DEBUG": True,
    "AUTO_RELOAD": True,
    "ACCESS_LOG": True,
    "HOST": "0.0.0.0",  # Allow external connections
    "PORT": 8000,
    "WEBSOCKET_MAX_SIZE": 2**20,  # 1MB
    "WEBSOCKET_PING_INTERVAL": 20,
    "WEBSOCKET_PING_TIMEOUT": 20,
    "REQUEST_MAX_SIZE": 2**20,  # 1MB
    "REQUEST_TIMEOUT": 60,  # 60 seconds
    "RESPONSE_TIMEOUT": 60,  # 60 seconds
    "KEEP_ALIVE_TIMEOUT": 60,  # 60 seconds
    "GRACEFUL_SHUTDOWN_TIMEOUT": 15.0,  # 15 seconds
})

# Configure logging
logger.remove()  # Remove default handler
logger.add(
    "logs/python.log",
    rotation="1 day",
    retention="7 days",
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    backtrace=True,
    diagnose=True
)
logger.add(
    sys.stderr,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    backtrace=True,
    diagnose=True
)

# Initialize authentication first (attaches AuthManager to app.ctx.auth)
init_auth(app)

# Initialize database (loads config and registers Tortoise)
init_db(app)

# Create blueprints for different route types
main_bp = Blueprint("main_http", url_prefix="/api")

# Create AI blueprint group using Blueprint.group()
ai_bp = Blueprint.group(
    ws_bp,  # WebSocket routes
    courses_bp,  # Course-related routes
    url_prefix="/ai"
)

# Register blueprints
app.blueprint(main_bp)  # Keep API routes separate
app.blueprint(ai_bp)  # Register the AI blueprint group

# Health check endpoint
@app.get("/api/health")
async def health_check(request):
    return json({"status": "healthy"})


@app.listener('after_server_start')
async def notify_server_started(app, loop):
    """Notify when server is ready and log all routes."""
    logger.info('Server started successfully!')
    # Disabled route logging to reduce log noise
    # log_routes(app)

@main_bp.route("/ai/health/")
async def ai_health_auth_check(request):
    if not request.ctx.user_id:
        return json_response({"error": "Authentication required for AI health check"}, status=401)
    return json_response({"health": "ok", "user_id": request.ctx.user_id, "message": "AI components are healthy"})

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
        auto_reload=True,
        access_log=True,
        workers=1  # Use single worker in development
    )