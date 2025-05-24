from ai_engine.apps.ai.llm import LLM
from ai_engine.apps.courses.models import Course
from langchain.schema import HumanMessage, SystemMessage
from uuid import UUID
from loguru import logger

from .chat import load_course_generator_prompt

async def generate_course_outline(course_id: str) -> str:
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
            
        # Load the system prompt
        system_prompt = load_course_generator_prompt()
        
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
        llm = LLM()
        return await llm.agenerate_response(messages)
        
    except Exception as e:
        logger.exception(f"Error generating course outline", course_id=course_id, error=str(e))
        raise