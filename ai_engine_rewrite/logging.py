"""
This module configures loguru for AI Engine.

To use this module, import it in your main file:

from .logging import logger
"""

import sys
from loguru import logger
from sanic import Sanic
# Configure logging
logger.remove()  # Remove default handler

logger.add(
    sys.stderr,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    backtrace=True,
    diagnose=True
)

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
