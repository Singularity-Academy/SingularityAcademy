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

async def generate_course_outline(course_id: str, llm: Optional[LLM] = None) -> str:
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
        # Load the course data
        course = await Course.filter(id=UUID(course_id)).first()
        if not course:
            logger.error(f"Course not found", course_id=course_id)
            raise ValueError(f"Course with ID {course_id} not found")
            
        # Load the system prompt using PromptLoader
        system_prompt = prompt_loader.get_prompt("course_generator")
        
        # Create the human message with course data
        course_data = {
            "name": course.name,
            "description": course.description,
            "created_at": course.created_at.isoformat(),
            "updated_at": course.updated_at.isoformat()
        }
        
        human_message = f"""Please generate a detailed course outline for the following course:

Course Name: {course_data['name']}
Course Description: {course_data['description']}

Please structure the outline with clear sections, learning objectives, and key topics to be covered.
Include practical exercises and assessments where appropriate."""

        # Create the message list
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_message)
        ]
        
        # Initialize LLM and generate response
        if not llm:
            llm = LLM()
        return await llm.agenerate_response(messages)
        
    except Exception as e:
        log_exception(e, f"Error generating course outline for course {course_id}")
        raise