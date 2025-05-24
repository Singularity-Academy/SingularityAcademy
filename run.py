"""
Run script for AI Engine Rewrite.
"""

import argparse
from ai_engine import app
from ai_engine.logging import logger, log_routes

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="AI Engine Rewrite Server")
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
    if args.log_level == "TRACE":
        log_routes(app)

    logger.info(f"Starting AI Engine in development mode on {args.host}:{args.port}")
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=True,
            auto_reload=True,
            access_log=True,
            workers=2  # Use single worker in development
        ) 
    except RuntimeError:
        pass
