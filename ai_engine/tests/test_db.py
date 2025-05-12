import asyncio
from tortoise import Tortoise
from ai_engine.db import User, load_db_config
import logging
import sys
from datetime import datetime

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'db_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

async def setup_database():
    """Initialize database connection."""
    try:
        db_config = load_db_config()
        db_url = f"mysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}"
        
        logger.info(f"Connecting to database at {db_config['host']}:{db_config['port']}")
        await Tortoise.init(
            db_url=db_url,
            modules={"models": ["ai_engine.db"]}
        )
        await Tortoise.generate_schemas()
        logger.info("Database connection established and schemas generated")
    except Exception as e:
        logger.error(f"Failed to setup database: {str(e)}")
        raise

async def test_database_connection():
    """Test database connection by trying to fetch a user."""
    try:
        logger.info("Testing database connection...")
        user = await User.all().first()
        if user:
            logger.info(f"Successfully connected to database. Found user: {user.username}")
        else:
            logger.info("Successfully connected to database. No users found.")
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        raise

async def test_load_users():
    """Load and display the first 10 users."""
    try:
        logger.info("Loading first 10 users...")
        users = await User.all().limit(10)
        
        logger.info(f"Found {len(users)} users:")
        if not users:
            logger.info("No users found in database")
            return
            
        for user in users:
            logger.info(
                f"User Details:\n"
                f"  ID: {user.id}\n"
                f"  Username: {user.username}\n"
                f"  Email: {user.email}\n"
                f"  Verified: {user.is_verified}\n"
                f"  Registered: {user.register_at}\n"
                f"  Verification Token: {user.verification_token or 'None'}"
            )
    except Exception as e:
        logger.error(f"Failed to load users: {str(e)}")
        raise

async def test_user_count():
    """Count and display total users."""
    try:
        logger.info("Counting total users...")
        count = await User.all().count()
        logger.info(f"Total users in database: {count}")
    except Exception as e:
        logger.error(f"Failed to count users: {str(e)}")
        raise

async def cleanup():
    """Clean up database connection."""
    try:
        logger.info("Closing database connections...")
        await Tortoise.close_connections()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        raise

async def main():
    """Run all database tests."""
    try:
        logger.info("Starting database tests...")
        await setup_database()
        
        await test_database_connection()
        await test_load_users()
        await test_user_count()
        
        logger.info("All tests completed successfully")
    except Exception as e:
        logger.error(f"Tests failed: {str(e)}")
        raise
    finally:
        await cleanup()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Tests interrupted by user")
    except Exception as e:
        logger.error(f"Tests failed with error: {str(e)}")
        sys.exit(1) 