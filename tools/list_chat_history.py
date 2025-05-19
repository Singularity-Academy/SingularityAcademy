#!/usr/bin/env python3
"""
Command-line tool to list chat history for a given email.

Usage:
    python list_chat_history.py <email>

Example:
    python list_chat_history.py user@example.com
"""

import sys
import asyncio
from datetime import datetime
from typing import Optional, List, Dict, Any
from loguru import logger
import ujson as json

# Add the project root to Python path
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_engine_rewrite.apps.principal.models import PrincipalChatHistory
from ai_engine_rewrite.apps.principal.chat import PrincipalChat
from ai_engine_rewrite.apps.auth.models import User
from ai_engine_rewrite.config import load_db_config, construct_db_url
from tortoise import Tortoise

async def init_db_connection():
    """Initialize database connection for the command-line tool."""
    try:
        db_config = load_db_config()
        db_url = construct_db_url(db_config)
        
        await Tortoise.init(
            db_url=db_url,
            modules={
                "models": [
                    "ai_engine_rewrite.apps.auth.models",
                    "ai_engine_rewrite.apps.principal.models"
                ]
            }
        )
        logger.info(f"Database connection initialized with URL: {db_url}")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def get_user_by_email(email: str) -> Optional[User]:
    """
    Get a user by their email address.
    
    Args:
        email: The email address to look up
        
    Returns:
        User object if found, None otherwise
    """
    try:
        return await User.get(email=email)
    except Exception as e:
        logger.error(f"Error finding user with email {email}: {e}")
        return None

async def get_chat_history(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Get chat history for a user.
    
    Args:
        user_id: The user's ID
        limit: Maximum number of messages to return
        
    Returns:
        List of chat messages
    """
    try:
        # Get chat instance using PrincipalChat
        chat = await PrincipalChat.get_by_user(user_id)
        if not chat:
            logger.error(f"Could not get chat instance for user {user_id}")
            return []
            
        # Initialize chat to ensure history is loaded
        await chat.initialize()
        
        # Format messages for display
        formatted_messages = []
        for msg in chat.history.messages:
            # Skip system messages
            if msg["role"] == "system":
                continue
                
            timestamp = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
            content = msg["content"]
            
            # Handle different content formats
            if isinstance(content, dict):
                # For assistant messages, content is a dict with text and calls
                text_content = content.get("text", "")
            else:
                # For user messages, content is a string
                text_content = content
                
            formatted_messages.append({
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "role": msg["role"],
                "content": text_content
            })
            
        # Return most recent messages first, limited by the limit parameter
        return formatted_messages[-limit:]
        
    except Exception as e:
        logger.error(f"Error getting chat history for user {user_id}: {e}")
        return []

def print_chat_history(messages: List[Dict[str, Any]]) -> None:
    """
    Print chat history in a readable format.
    
    Args:
        messages: List of formatted chat messages
    """
    if not messages:
        print("No chat history found.")
        return
        
    print("\nChat History:")
    print("=" * 80)
    
    for msg in messages:
        role = msg["role"].upper()
        timestamp = msg["timestamp"]
        content = msg["content"]
        
        # Format the message with clear role and timestamp
        print(f"\n[{timestamp}] {role}:")
        print("-" * 40)
        print(content)
        print("-" * 80)

async def main():
    """Main entry point for the script."""
    if len(sys.argv) != 2:
        print("Usage: python list_chat_history.py <email>")
        sys.exit(1)
        
    email = sys.argv[1]
    
    try:
        # Initialize database connection
        await init_db_connection()
        
        # Get user
        user = await get_user_by_email(email)
        if not user:
            print(f"Error: No user found with email {email}")
            sys.exit(1)
            
        # Get and print chat history
        messages = await get_chat_history(user.id)
        print(f"\nChat history for {email} (User ID: {user.id})")
        print_chat_history(messages)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    finally:
        # Close database connection
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
    asyncio.run(main()) 