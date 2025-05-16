from sanic import Blueprint, json
from sanic.exceptions import SanicException
from tortoise.exceptions import DoesNotExist, ValidationError
from loguru import logger
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from .auth import AuthManager, login_required
from .db import Course, User
from .exceptions import AIEngineError, ValidationError as AIValidationError

# Configure loguru
logger.remove()  # Remove default handler
logger.add(
    "logs/courses.log",
    rotation="500 MB",
    retention="10 days",
    compression="zip",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    backtrace=True,
    diagnose=True
)
logger.add(
    lambda msg: print(msg, end=""),  # Also print to console
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    backtrace=True,
    diagnose=True
)

bp = Blueprint("courses", url_prefix="/courses")
bp.ctx.auth = AuthManager

# Custom exceptions for course-related errors
class CourseError(AIEngineError):
    """Base exception for course-related errors."""
    def __init__(self, message: str, error_code: str = "COURSE_ERROR", status_code: int = 500):
        super().__init__(message, error_code, status_code)

class CourseNotFoundError(CourseError):
    """Raised when a course is not found."""
    def __init__(self, course_id: Optional[int] = None, name: Optional[str] = None):
        if course_id:
            message = f"Course with ID {course_id} not found"
        elif name:
            message = f"Course '{name}' not found"
        else:
            message = "Course not found"
        super().__init__(message, "COURSE_NOT_FOUND", 404)

class CourseValidationError(CourseError):
    """Raised when course validation fails."""
    def __init__(self, message: str):
        super().__init__(message, "COURSE_VALIDATION_ERROR", 400)

# Helper functions
def format_course_response(course: Course) -> Dict[str, Any]:
    """Format a course object into a response dictionary."""
    return {
        "id": course.id,
        "name": course.name,
        "description": course.desc,
        "created_at": course.created_at.isoformat(),
        "owner_id": course.owner_id
    }

def validate_course_data(data: Dict[str, Any], is_update: bool = False) -> Dict[str, Any]:
    """Validate course data for creation or update."""
    validated = {}
    
    # Name validation
    if "name" in data:
        name = data["name"].strip()
        if not name:
            raise CourseValidationError("Course name cannot be empty")
        if len(name) > 255:
            raise CourseValidationError("Course name must be less than 255 characters")
        validated["name"] = name
    
    # Description validation
    if "description" in data:
        desc = data["description"]
        if desc is not None and not isinstance(desc, str):
            raise CourseValidationError("Description must be a string")
        validated["desc"] = desc
    
    # For updates, require at least one field to be present
    if is_update and not validated:
        raise CourseValidationError("No valid fields provided for update")
    
    return validated

# Route handlers
@bp.get("/all")
@login_required
async def get_courses(request):
    """Get all courses for the authenticated user."""
    try:
        user_id = request.ctx.user_id
        logger.info("Fetching courses for user {}", user_id)
        
        # Query courses from database
        courses = await Course.filter(owner_id=user_id).prefetch_related('owner')
        
        # Format response
        response = {
            "courses": [format_course_response(course) for course in courses],
            "count": len(courses),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        logger.success("Successfully fetched {} courses for user {}", len(courses), user_id)
        return json(response)
        
    except Exception as e:
        logger.exception("Error fetching courses for user {}: {}", request.ctx.user_id, str(e))
        if isinstance(e, CourseError):
            return json({"error": e.message, "error_code": e.error_code}, status=e.status_code)
        return json({"error": "Failed to fetch courses", "error_code": "INTERNAL_ERROR"}, status=500)

@bp.post("/create")
@login_required
async def create_course(request):
    """Create a new course."""
    try:
        user_id = request.ctx.user_id
        data = request.json
        
        if not data:
            raise CourseValidationError("No data provided")
        
        # Validate course data
        validated_data = validate_course_data(data)
        
        # Create course
        course = await Course.create(
            owner_id=user_id,
            **validated_data
        )
        
        logger.success("Created new course '{}' (ID: {}) for user {}", course.name, course.id, user_id)
        return json(format_course_response(course), status=201)
        
    except CourseValidationError as e:
        logger.warning("Course validation error: {}", str(e))
        return json({"error": e.message, "error_code": e.error_code}, status=e.status_code)
    except Exception as e:
        logger.exception("Error creating course for user {}: {}", request.ctx.user_id, str(e))
        return json({"error": "Failed to create course", "error_code": "INTERNAL_ERROR"}, status=500)

@bp.get("/<course_id:int>")
@login_required
async def get_course(request, course_id: int):
    """Get a specific course by ID."""
    try:
        user_id = request.ctx.user_id
        logger.info("Fetching course {} for user {}", course_id, user_id)
        
        # Get course and verify ownership
        course = await Course.get_or_none(id=course_id, owner_id=user_id)
        if not course:
            raise CourseNotFoundError(course_id=course_id)
        
        logger.success("Successfully fetched course {}", course_id)
        return json(format_course_response(course))
        
    except CourseNotFoundError as e:
        logger.warning("Course not found: {}", str(e))
        return json({"error": e.message, "error_code": e.error_code}, status=e.status_code)
    except Exception as e:
        logger.exception("Error fetching course {}: {}", course_id, str(e))
        return json({"error": "Failed to fetch course", "error_code": "INTERNAL_ERROR"}, status=500)

@bp.put("/<course_id:int>")
@login_required
async def update_course(request, course_id: int):
    """Update a specific course."""
    try:
        user_id = request.ctx.user_id
        data = request.json
        
        if not data:
            raise CourseValidationError("No data provided for update")
        
        # Get course and verify ownership
        course = await Course.get_or_none(id=course_id, owner_id=user_id)
        if not course:
            raise CourseNotFoundError(course_id=course_id)
        
        # Validate update data
        validated_data = validate_course_data(data, is_update=True)
        
        # Update course
        await course.update_from_dict(validated_data).save()
        
        logger.success("Updated course {} for user {}", course_id, user_id)
        return json(format_course_response(course))
        
    except CourseNotFoundError as e:
        logger.warning("Course not found: {}", str(e))
        return json({"error": e.message, "error_code": e.error_code}, status=e.status_code)
    except CourseValidationError as e:
        logger.warning("Course validation error: {}", str(e))
        return json({"error": e.message, "error_code": e.error_code}, status=e.status_code)
    except Exception as e:
        logger.exception("Error updating course {}: {}", course_id, str(e))
        return json({"error": "Failed to update course", "error_code": "INTERNAL_ERROR"}, status=500)

@bp.delete("/<course_id:int>")
@login_required
async def delete_course(request, course_id: int):
    """Delete a specific course."""
    try:
        user_id = request.ctx.user_id
        logger.info("Attempting to delete course {} for user {}", course_id, user_id)
        
        # Get course and verify ownership
        course = await Course.get_or_none(id=course_id, owner_id=user_id)
        if not course:
            raise CourseNotFoundError(course_id=course_id)
        
        # Delete course
        await course.delete()
        
        logger.success("Successfully deleted course {}", course_id)
        return json({"message": "Course deleted successfully"})
        
    except CourseNotFoundError as e:
        logger.warning("Course not found: {}", str(e))
        return json({"error": e.message, "error_code": e.error_code}, status=e.status_code)
    except Exception as e:
        logger.exception("Error deleting course {}: {}", course_id, str(e))
        return json({"error": "Failed to delete course", "error_code": "INTERNAL_ERROR"}, status=500)