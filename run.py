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
        default="INFO",
        choices=["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level"
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
    
    logger.info("Starting AI Engine in development mode")
    app.run(host="0.0.0.0", port=8000, access_log=True)
