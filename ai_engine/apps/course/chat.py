"""
Chat implementation for course interactions.

This module provides the CourseChat class for managing chat interactions
within courses, including message history and AI assistance.
"""

import datetime
from typing import List, Optional, Dict, Any
from loguru import logger
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from .models import Course
from ai_engine.apps.ai.llm import LLM
from ai_engine.apps.ai.prompt_loader import default_loader as prompt_loader

# Load course-specific prompts
try:
    COURSE_TUTOR_PROMPT = prompt_loader.get_prompt("course_tutor")
except FileNotFoundError as e:
    logger.error(f"Failed to load course tutor prompt: {e}")
    COURSE_TUTOR_PROMPT = "You are an expert tutor for this course, helping students understand the material."

class CourseChat:
    """
    Manages chat interactions within a course.
    To initialize, use CourseChat.get_by_course(course_id).
    """
    def __init__(self, course_obj: Course):
        if not isinstance(course_obj, Course):
            raise ValueError("course_obj must be an instance of Course")
        self.course = course_obj
        self.langchain_messages: List[HumanMessage | AIMessage | SystemMessage] = []
        self.initialized = False
        self.llm = LLM()

    async def initialize(self):
        """Initialize the chat by loading message history and setting up the tutor."""
        if not self.initialized:
            await self._load_history()
            # If no messages exist, add the system prompt with course context
            if not self.course.chat_history:
                system_message = self._create_system_message()
                self.course.chat_history = [system_message]
                await self.course.save()
                self.langchain_messages.append(SystemMessage(content=system_message["content"]))
            self.initialized = True

    def _create_system_message(self) -> dict:
        """Create a system message with course context."""
        # Format the outline sections
        outline_text = "\nCourse Outline:\n"
        for section in self.course.outline:
            outline_text += f"\n{section['order']}. {section['title']}\n"
            outline_text += f"   {section['description']}\n"

        course_context = f"""
        You are an expert tutor for the course: {self.course.name}
        Course Description: {self.course.description}
        Difficulty Level: {self.course.difficulty}
        Estimated Hours: {self.course.estimated_hours}
        
        {outline_text}
        
        {COURSE_TUTOR_PROMPT}
        
        When answering questions:
        1. Reference specific sections of the course outline when relevant
        2. Maintain the difficulty level appropriate for this course
        3. Provide examples and explanations that align with the course content
        4. If a question is outside the course scope, politely redirect to relevant course material
        """
        return self.create_message("system", course_context, datetime.datetime.now().isoformat())

    async def _load_history(self):
        """Load chat history into langchain message format."""
        for message in self.course.chat_history:
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

    async def add_message(self, message: str, role: str = "user"):
        """
        Add a new message to the course chat history.
        
        Args:
            message: The message content
            role: Either 'user' or 'assistant'
        """
        if not self.initialized:
            await self.initialize()
        
        new_message = self.create_message(role, message, datetime.datetime.now().isoformat())
        self.course.chat_history.append(new_message)
        await self.course.save()
        await self.course.update_last_accessed()
        
        if role == "user":
            self.langchain_messages.append(HumanMessage(content=message))
        elif role == "assistant":
            self.langchain_messages.append(AIMessage(content=message))

    @staticmethod
    def create_message(role: str, content: str, timestamp: str) -> dict:
        """Create a message dictionary."""
        return {
            "message_id": f"{role}-{datetime.datetime.now().timestamp()}",
            "role": role,
            "content": content,
            "timestamp": timestamp
        }
    
    @classmethod
    async def get_by_course(cls, course_id: str) -> Optional["CourseChat"]:
        """
        Get a CourseChat instance for a course.
        
        Args:
            course_id: The UUID of the course
            
        Returns:
            CourseChat instance if found, None if error
        """
        try:
            course = await Course.get_or_none(id=course_id)
            if not course:
                logger.error(f"Course not found: {course_id}")
                return None
            
            chat = cls(course)
            await chat.initialize()
            return chat
            
        except Exception as e:
            logger.error(f"Error getting chat for course {course_id}: {str(e)}")
            return None

    async def reset(self) -> None:
        """
        Reset the chat history to only contain the system prompt.
        """
        try:
            system_message = self._create_system_message()
            self.course.chat_history = [system_message]
            await self.course.save()
            
            self.langchain_messages = [SystemMessage(content=system_message["content"])]
            self.initialized = True
            
            logger.info(f"Chat history reset for course {self.course.id}")
        except Exception as e:
            logger.error(f"Error resetting chat history: {e}")
            raise

    async def get_recent_messages(self, limit: int = 10) -> List[dict]:
        """Get the most recent chat messages."""
        if not self.course.chat_history:
            return []
        return self.course.chat_history[-limit:] 