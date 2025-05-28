"""
This module configures loguru for AI Engine.

To use this module, import it in your main file:

from .logging import logger, configure_logging
"""

import sys
import traceback
from loguru import logger
from sanic import Sanic

__all__ = [
    'logger',
    'log_exception',
    'log_routes',
    'configure_logging'
]

def configure_logging(log_level: str = "DEBUG") -> None:
    """
    Configure the logging level for the application.
    
    Args:
        log_level: The logging level to use. Must be one of:
                  "TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"
    """
    # Remove default handler
    logger.remove()
    
    # Add new handler with specified log level
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        backtrace=True,
        diagnose=True
    )
    
    logger.info(f"Logging configured with level: {log_level}")

# Configure default logging
configure_logging()

def log_exception(e: Exception, msg: str = None) -> None:
    """
    Log an exception with optional message, printing traceback only if logger level is TRACE.
    
    Args:
        e: The exception to log
        msg: Optional message to include with the exception
    """
    if msg:
        logger.error(f"{msg}: {str(e)}")
    else:
        logger.error(str(e))
    
    # Only print traceback if logger level is TRACE
    if logger.level("TRACE").no <= logger.level("DEBUG").no:  # Compare with DEBUG level
        traceback.print_exc()

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
