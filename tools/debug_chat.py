#!/usr/bin/env python3
"""
Debug CLI for Chat object.
This module provides a command-line interface for testing the Chat functionality
with detailed logging.

Usage:
    python tools/debug_chat.py <email>

Example:
    python tools/debug_chat.py user@example.com
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger
from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist

from ai_engine.db import User, PrincipalChatHistory, load_db_config
from ai_engine.ai import Chat
from ai_engine.model_config import model_manager

# Configure logger for TRACE level
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="TRACE",
    colorize=True
)

# Ensure logs directory exists
logs_dir = project_root / "logs"
logs_dir.mkdir(exist_ok=True)

logger.add(
    logs_dir / "debug_chat.log",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    level="TRACE",
    rotation="1 day",
    retention="7 days"
)

async def init_db():
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

async def get_user_by_email(email: str) -> User:
    """Get user by email address."""
    try:
        user = await User.get(email=email)
        logger.debug(f"Found user: {user.id} ({user.email})")
        return user
    except DoesNotExist:
        logger.error(f"User not found: {email}")
        return None

async def list_available_models():
    """List all available models."""
    models = model_manager.list_models()
    logger.info("Available models:")
    for model_id in models:
        model_config = model_manager.get_model_config(model_id)
        if model_config:
            logger.info(f"  - {model_id}: {model_config.name}")
        else:
            logger.info(f"  - {model_id}")

async def chat_session(user: User):
    """Run an interactive chat session."""
    logger.trace("Starting chat session initialization")
    logger.info(f"Starting chat session for user {user.id} ({user.email})")
    
    try:
        # Get or create chat instance
        logger.trace(f"Looking for existing chat history for user {user.id}")
        history, created = await PrincipalChatHistory.get_or_create(
            user=user,
            defaults={"title": "Debug Chat Session"}
        )
        logger.debug(f"Chat history {'created' if created else 'loaded'}: {history.id}")
        logger.trace(f"History details - ID: {history.id}, Messages: {len(history.messages)}")
        
        # Create chat instance with existing history
        logger.trace(f"Creating Chat instance with user ID {user.id} and history ID {history.id}")
        chat = Chat(user, history.id)
        logger.debug("Chat instance created")
        logger.trace(f"Chat initialized with model: {chat.model_config.model_id} ({chat.model_config.name})")
        
        # List available models
        logger.trace("Listing available models")
        await list_available_models()
        
        # Print chat history (excluding system messages)
        logger.trace("Loading chat history messages")
        messages = await chat.get_history_messages()
        if messages:
            logger.info("Previous messages:")
            for idx, msg in enumerate(messages):
                role = msg.get("role", "unknown")
                if role == "system":
                    logger.trace(f"Skipping system message at index {idx}")
                    continue
                content = msg.get("content", "")
                if isinstance(content, dict):
                    logger.trace(f"Processing complex message at index {idx}")
                    content = content.get("text", str(content))
                logger.info(f"[{role}] {content}")
                logger.trace(f"Message {idx} details: Role={role}, Content length={len(content)}")
        
        # Interactive loop
        logger.trace("Entering interactive loop")
        logger.info("\nStarting interactive chat (type 'exit' to quit, 'model <id>' to switch models)")
        while True:
            try:
                # Get user input
                logger.trace("Waiting for user input")
                user_input = input("\nYou: ").strip()
                logger.trace(f"Received input: {user_input[:50]}... (length: {len(user_input)})")
                
                # Check for commands
                if user_input.lower() == "exit":
                    logger.trace("User requested exit")
                    logger.info("Exiting chat session")
                    break
                elif user_input.lower().startswith("model "):
                    model_id = user_input[6:].strip()
                    logger.trace(f"Model switch requested: {model_id}")
                    old_model = chat.model_config.model_id
                    if chat.update_model(model_id):
                        logger.info(f"Switched to model: {model_id}")
                        logger.trace(f"Model switch successful: {old_model} -> {model_id}")
                    else:
                        logger.error(f"Failed to switch to model: {model_id}")
                        logger.trace("Model switch failed, maintaining current model")
                    continue
                
                # Process message
                logger.debug(f"Processing message: {user_input}")
                logger.trace("Starting message processing pipeline")
                async for chunk in chat.stream_message(user_input):
                    logger.trace(f"Received stream chunk: {chunk.content[:20]}... (final: {chunk.is_final}, error: {bool(chunk.error)})")
                    if chunk.error:
                        logger.error(f"Error in stream chunk: {chunk.error}")
                        raise Exception(chunk.error)
                    print(chunk.content, end="", flush=True)
                    if chunk.is_final:
                        print()
                        logger.trace("Final chunk processed, resetting buffer")
                
            except KeyboardInterrupt:
                logger.trace("Keyboard interrupt received")
                logger.info("\nChat session interrupted")
                break
            except Exception as e:
                logger.error(f"Error in chat session: {e}")
                logger.trace(f"Error details: {str(e)}")
                import traceback
                traceback.print_exc()
                # Continue to the next iteration rather than exiting
                continue
            
    except Exception as e:
        logger.error(f"Fatal error in chat session: {e}")
        logger.trace(f"Fatal error context: User ID {user.id}, History ID {getattr(history, 'id', None)}")
        import traceback
        traceback.print_exc()
        raise  # Re-raise to be handled by main()

async def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python tools/debug_chat.py <email>")
        sys.exit(1)
    
    email = sys.argv[1]
    logger.info(f"Looking up user: {email}")
    
    try:
        # Initialize database connection
        await init_db()
        logger.debug("Database initialized")
        
        # Get user
        user = await get_user_by_email(email)
        if not user:
            logger.error(f"User not found: {email}")
            sys.exit(1)
        
        # Start chat session
        await chat_session(user)
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Close database connection
        await Tortoise.close_connections()
        logger.debug("Database connection closed")

if __name__ == "__main__":
    asyncio.run(main()) 