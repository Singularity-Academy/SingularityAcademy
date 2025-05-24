"""
Chat implementation for the principal AI system.

This module provides the PrincipalChat class for managing chat interactions
with the principal AI, including message history and langchain integration.
"""

import datetime
import os
from ujson import dumps
from pathlib import Path
from typing import List, Optional
from loguru import logger
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from ai_engine.apps.courses.models import Course

from .models import PrincipalChatHistory

def load_principal_prompt() -> str:
    """
    Load the Principal's prompt from the prompt.txt file.
    
    The prompt file is located in the same directory as this module.
    
    Returns:
        str: The contents of the prompt file
        
    Raises:
        FileNotFoundError: If prompt.txt is not found
        IOError: If there are issues reading the file
    """
    # Get the directory containing this module
    current_dir = Path(__file__).parent
    prompt_path = current_dir / "prompt.txt"
    
    try:
        with open(prompt_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Prompt file not found at {prompt_path}")
    except IOError as e:
        logger.error(f"Error reading prompt file: {e}")
    return ""


def load_course_generator_prompt() -> str:
    """
    Load the Principal's prompt from the prompt.txt file.
    
    The prompt file is located in the same directory as this module.
    
    Returns:
        str: The contents of the prompt file
        
    Raises:
        FileNotFoundError: If prompt.txt is not found
        IOError: If there are issues reading the file
    """
    # Get the directory containing this module
    current_dir = Path(__file__).parent
    prompt_path = current_dir / "course_prompt.txt"
    
    try:
        with open(prompt_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Prompt file not found at {prompt_path}")
    except IOError as e:
        logger.error(f"Error reading prompt file: {e}")
    return ""
class PrincipalChat:
    """
    Wrapper around the PrincipalChatHistory model.
    To init, use PrincipalChat.get_by_user(user_id).
    """
    def __init__(self, history_obj: PrincipalChatHistory):
        if not isinstance(history_obj, PrincipalChatHistory):
            raise ValueError("history_obj must be an instance of PrincipalChatHistory")
        self.history = history_obj
        self.langchain_messages: List[HumanMessage | AIMessage | SystemMessage] = []
        self.initialized = False

    async def initialize(self):
        """Initialize the chat by loading message history."""
        print(self.history.messages)
        if not self.initialized:
            await self._load_history()
            # If no messages exist, add the system prompt
            if not self.history.messages:
                system_message = self.create_message("system", load_principal_prompt(), datetime.datetime.now().isoformat())
                self.history.messages = [system_message]
                await self.history.save()
                self.langchain_messages.append(SystemMessage(content=load_principal_prompt()))
            self.initialized = True

    async def _load_history(self):
        """Load chat history into langchain message format."""
        for message in self.history.messages:
            #logger.info(f"{message}")
            role = message.get("role")
            content = message.get("content")
            
            if role == "user":
                self.langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                self.langchain_messages.append(AIMessage(content=content))
            elif role == "system":
                self.langchain_messages.append(SystemMessage(content=content))
            else:
                logger.warning(f"Unknown message role: {role}")

    async def add_message(self, message: str, role: str):
        """Add a new message to the chat history."""
        if not self.initialized:
            await self.initialize()
        
        new_message = {
            "role": role,
            "content": message,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.history.messages.append(new_message)
        await self.history.save()
        
        if role == "user":
            self.langchain_messages.append(HumanMessage(content=message))
        elif role == "assistant":
            self.langchain_messages.append(AIMessage(content=message))
        elif role == "system":
            self.langchain_messages.append(SystemMessage(content=message))

    @staticmethod
    def create_message(role: str, content: str, timestamp: str) -> dict:
        """Create a message dictionary."""
        return {
            "role": role,
            "content": content,
            "timestamp": timestamp
        }
    
    @classmethod
    async def get_by_user(cls, user_id: str) -> Optional["PrincipalChat"]:
        """
        Get or create a PrincipalChat instance for a user.
        
        Args:
            user_id: The UUID of the user
            
        Returns:
            PrincipalChat instance if found or created, None if error
        """
        try:
            # Try to find existing history
            history = await PrincipalChatHistory.filter(user_id=user_id).first()
            
            if not history:
                # Create new history if none exists
                history = await PrincipalChatHistory.create(
                    user_id=user_id,
                    messages=[]  # Start with empty messages, system prompt will be added during initialization
                )
                logger.info(f"Created new chat history for user {user_id}")
            
            chat = cls(history)
            
            #logger.info(f"Chat history: {chat.history.messages}")
            await chat.initialize()  # Initialize the chat instance
            return chat
            
        except Exception as e:
            logger.error(f"Error getting/creating chat for user {user_id}: {str(e)}")
            return None

    @classmethod
    async def new(cls, user_id: int):
        """Create a new chat instance for a user."""
        history = await PrincipalChatHistory.create(user_id=user_id)
        history.messages = [cls.create_message("system", load_principal_prompt(), datetime.now().isoformat())]
        await history.save()
        obj = cls(history)
        return obj

    
    
