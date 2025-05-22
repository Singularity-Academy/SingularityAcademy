from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from ai_engine.apps.courses.models import Course
from tortoise.exceptions import DoesNotExist
from ai_engine.logging import logger

# Request validation models
class CourseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)

class CourseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)

    @field_validator('name', 'description')
    @classmethod
    def validate_not_empty(cls, v):
        if v is not None and not v.strip():
            logger.warning("Empty field value detected in course update")
            raise ValueError('Field cannot be empty')
        return v

# Helper function to get course with ownership check
async def get_course_with_ownership(user_id: UUID, course_id: UUID) -> Optional[Course]:
    try:
        course = await Course.filter(user_id=user_id, id=course_id).first()
        if course:
            logger.debug("Course found", course_id=str(course.id), user_id=str(user_id))
        else:
            logger.debug("No course found", course_id=str(course_id), user_id=str(user_id))
        return course
    except DoesNotExist:
        logger.debug("Course does not exist", course_id=str(course_id))
        return None
    except Exception as e:
        logger.exception("Error checking course ownership", course_id=str(course_id), user_id=str(user_id))
        raise

# Helper function to format course response
def format_course_response(course: Course) -> dict:
    try:
        response = {
            "id": str(course.id),
            "name": course.name,
            "description": course.description,
            "created_at": course.created_at.isoformat(),
            "updated_at": course.updated_at.isoformat()
        }
        logger.debug("Formatted course response", course_id=str(course.id))
        return response
    except Exception as e:
        logger.exception("Error formatting course response", course_id=str(course.id))
        raise 