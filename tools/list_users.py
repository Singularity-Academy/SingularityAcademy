"""
Simple script to list all users and their emails from the database.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from tortoise import Tortoise
from ai_engine.apps.auth.models import User
from ai_engine.config import load_db_config, construct_db_url
from loguru import logger

async def init_db():
    """Initialize database connection using configuration from ai_engine/config."""
    try:
        # Load database configuration
        db_config = load_db_config()
        db_url = construct_db_url(db_config)
        
        # Initialize Tortoise with all models
        await Tortoise.init(
            db_url=db_url,
            modules={
                'models': [
                    'ai_engine.apps.auth.models',
                    'ai_engine.apps.course.models'
                ]
            }
        )
        logger.info(f"Connected to database at {db_config['host']}:{db_config['port']}")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def list_users():
    """List all users and their emails."""
    try:
        # Initialize database
        await init_db()
        print("Database initialized")
        
        # Get all users
        users = await User.all()
        
        if not users:
            print("No users found in database")
            return
            
        print("\nUsers in database:")
        print("-" * 50)
        print(f"{'ID':<5} {'Email':<40} {'Username':<20}")
        print("-" * 50)
        
        for user in users:
            print(f"{user.id:<5} {user.email:<40} {user.username:<20}")
            
    except Exception as e:
        logger.error(f"Error listing users: {e}")
    finally:
        await Tortoise.close_connections()

if __name__ == "__main__":
    # Configure logging
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # Run the async main function
    asyncio.run(list_users()) 