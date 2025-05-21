#!/usr/bin/env python3
"""
Script to drop the chat history table.
This is a one-time operation to clean up the database.

Usage:
    python tools/drop_chat_history.py
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger
from tortoise import Tortoise
from tortoise.exceptions import OperationalError

from ai_engine.config import load_db_config
from ai_engine.registry import get_modules

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO",
    colorize=True
)

async def init_db():
    """Initialize database connection."""
    try:
        db_config = load_db_config()
        db_url = f"mysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}"
        
        logger.info(f"Connecting to database at {db_config['host']}:{db_config['port']}")
        modules = get_modules()
        l = []
        for key, items in modules.items():
            for item in items:
                if item.endswith("models"):
                    l.append(item)
        await Tortoise.init(
            db_url=db_url,
            modules={"models": l}
        )
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Failed to setup database: {str(e)}")
        raise

async def drop_chat_history():
    """Drop the chat history table."""
    try:
        # Drop only the PrincipalChatHistory table
        await Tortoise.get_connection("default").execute_query(
            "DROP TABLE IF EXISTS principal_chat_history"
        )
        logger.info("Successfully dropped principal_chat_history table")
    except OperationalError as e:
        logger.error(f"Failed to drop table: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

async def main():
    """Main entry point."""
    try:
        # Initialize database connection
        await init_db()
        
        # Confirm with user
        response = input("This will drop the chat history table. Are you sure? (yes/no): ")
        if response.lower() != "yes":
            logger.info("Operation cancelled by user")
            return
        
        # Drop the table
        await drop_chat_history()
        
    except Exception as e:
        logger.exception("Fatal error")
        sys.exit(1)
    finally:
        # Close database connection
        await Tortoise.close_connections()
        logger.debug("Database connection closed")

if __name__ == "__main__":
    asyncio.run(main()) 