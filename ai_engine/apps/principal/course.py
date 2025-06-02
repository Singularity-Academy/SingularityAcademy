"""Course planning module for the principal app."""

from typing import Dict, Any, Optional
from loguru import logger
import json

from ai_engine.apps.ai.llm import LLM
from ai_engine.apps.ai.prompt_loader import default_loader as prompt_loader
from ai_engine.apps.course.models import Course
from langchain.schema import HumanMessage, SystemMessage
from uuid import UUID
from ai_engine.logging import log_exception

async def generate_course_outline(course_data: dict, llm: Optional[LLM] = None) -> str:
    """
    Generate a course outline for a given course ID.
    
    Args:
        course_id (str): The UUID of the course to generate an outline for
        
    Returns:
        str: The generated course outline
        
    Raises:
        ValueError: If the course is not found
    """
    try:  
        # Load the system prompt using PromptLoader
        system_prompt = prompt_loader.get_prompt("course_generator")

        human_message = f"""Please generate a detailed course outline for the following course:\nCourse Name: {course_data['name']}\nCourse Description: {course_data['description']}\n"""

        # Create the message list
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_message)
        ]
        
        # Initialize LLM and generate response
        if not llm:
            llm = LLM()
        response = await llm.agenerate_response(messages)
        # Strip code block markers if present
        response = response.strip()
        if response.startswith("```"):
            # Remove leading triple backticks and optional 'json' language tag
            response = response.lstrip("`").lstrip("json").strip()
            # Remove trailing triple backticks if present
            if response.endswith("```"):
                response = response.rstrip("```").strip()
        return response
        
    except Exception as e:
        log_exception(e, f"Error generating course outline for course {course_data['name']}")
        raise