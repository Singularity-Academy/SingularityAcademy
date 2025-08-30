"""
Chat implementation for the principal AI system.

This module provides the PrincipalChat class for managing chat interactions
with the principal AI, including message history and langchain integration.
"""

import datetime
import os
import ujson as json
from ujson import dumps
from pathlib import Path
from typing import List, Optional, Dict, Any
from loguru import logger
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from .models import PrincipalChatHistory
from ai_engine.apps.ai.llm import LLM
from ai_engine.apps.ai.prompt_loader import default_loader as prompt_loader

# Load prompts at module level using PromptLoader
try:
    PRINCIPAL_PROMPT = prompt_loader.get_prompt("principal")
    COURSE_GENERATOR_PROMPT = prompt_loader.get_prompt("course_generator")
except FileNotFoundError as e:
    logger.error(f"Failed to load required prompts: {e}")
    PRINCIPAL_PROMPT = "You are an expert educational AI assistant."
    COURSE_GENERATOR_PROMPT = "You are an expert educational course planner."

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
        self.llm = LLM()

    async def initialize(self):
        """Initialize the chat by loading message history."""
        print(self.history.messages)
        if not self.initialized:
            await self._load_history()
            # If no messages exist, add the system prompt
            if not self.history.messages:
                system_message = self.create_message("system", PRINCIPAL_PROMPT, datetime.datetime.now().isoformat())
                self.history.messages = [system_message]
                await self.history.save()
                self.langchain_messages.append(SystemMessage(content=PRINCIPAL_PROMPT))
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

    async def add_message(self, message: str, role: str, courses: Optional[List[Dict[str, Any]]] = None):
        """Add a new message to the chat history."""
        if not self.initialized:
            await self.initialize()
        
        new_message = {
            "role": role,
            "content": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "courses": courses or []
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

       
    async def reset(self) -> None:
        """
        Reset the chat history to only contain the system prompt.
        
        This method:
        1. Clears all messages except the system prompt
        2. Resets the langchain messages list
        3. Reinitializes the chat with just the system prompt
        """
        try:
            # Keep only the system prompt
            system_message = self.create_message("system", PRINCIPAL_PROMPT, datetime.datetime.now().isoformat())
            self.history.messages = [system_message]
            await self.history.save()
            
            # Reset langchain messages
            self.langchain_messages = [SystemMessage(content=PRINCIPAL_PROMPT)]
            self.initialized = True
            
            logger.info(f"Chat history reset for user {self.history.user_id}")
        except Exception as e:
            logger.error(f"Error resetting chat history: {e}")
            raise

    
    
