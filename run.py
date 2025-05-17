"""
Run script for AI Engine.
"""

import sys
import argparse
from loguru import logger
from ai_engine import app

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="AI Engine Server")
    parser.add_argument(
        "--log-level",
        default="DEBUG",  # Changed default to DEBUG for development
        choices=["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind the server to"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the server to"
    )
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_args()
    
    # Configure logging
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        level=args.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    logger.info(f"Starting AI Engine in development mode on {args.host}:{args.port}")
    app.run(
        host=args.host,
        port=args.port,
        debug=True,
        auto_reload=True,
        access_log=True,
        workers=1  # Use single worker in development
    )
