from sanic import Blueprint, response
from ai_engine.apps.auth import login_required
from ai_engine.apps.courses.models import Course
from ai_engine.apps.courses.utils import (
    CourseCreate, CourseUpdate, get_course_with_ownership, format_course_response
)
from sanic.response import json
from tortoise.exceptions import DoesNotExist, IntegrityError
from uuid import UUID
from ai_engine.logging import logger

bp = Blueprint("courses", url_prefix="/courses")

# GET /courses/all - List all courses for the user
@bp.get("/all")
@login_required
async def get_courses(request):
    user_id = request.ctx.user_id
    try:
        courses = await Course.filter(user_id=user_id).all()
        logger.info("Fetched all courses", user_id=str(user_id), count=len(courses))
        return json([format_course_response(course) for course in courses])
    except Exception as e:
        logger.exception("Error fetching courses", user_id=str(user_id))
        raise

# GET /courses/<course_id> - Get a specific course
@bp.get("/<course_id:uuid>")
@login_required
async def get_course(request, course_id: UUID):
    user_id = request.ctx.user_id
    try:
        course = await get_course_with_ownership(user_id, course_id)
        
        if not course:
            logger.warning("Course not found", course_id=str(course_id), user_id=str(user_id))
            return json({"error": "Course not found"}, status=404)
        
        logger.info("Successfully fetched course", course_id=str(course_id), user_id=str(user_id))
        return json(format_course_response(course))
    except Exception as e:
        logger.exception("Error fetching course", course_id=str(course_id), user_id=str(user_id))
        raise

# POST /courses/new - Create a new course
@bp.post("/new")
@login_required
async def create_course(request):
    user_id = request.ctx.user_id
    try:
        # Validate request data
        data = CourseCreate(**request.json)
        logger.debug("Validated course creation data", user_id=str(user_id))
        
        # Create course
        course = await Course.create(
            user_id=user_id,
            name=data.name,
            description=data.description
        )
        
        logger.info("Successfully created course", course_id=str(course.id), user_id=str(user_id))
        return json(format_course_response(course), status=201)
        
    except ValueError as e:
        logger.warning("Validation error creating course", error=str(e), user_id=str(user_id))
        return json({"error": str(e)}, status=400)
    except IntegrityError as e:
        logger.exception("Database error creating course", user_id=str(user_id))
        return json({"error": "Database error occurred"}, status=500)
    except Exception as e:
        logger.exception("Unexpected error creating course", user_id=str(user_id))
        raise

# PUT /courses/<course_id> - Update a course
@bp.put("/<course_id:uuid>")
@login_required
async def update_course(request, course_id: UUID):
    user_id = request.ctx.user_id
    try:
        course = await get_course_with_ownership(user_id, course_id)
        
        if not course:
            logger.warning("Course not found for update", course_id=str(course_id), user_id=str(user_id))
            return json({"error": "Course not found"}, status=404)
        
        # Validate request data
        data = CourseUpdate(**request.json)
        logger.debug("Validated course update data", course_id=str(course_id), user_id=str(user_id))
        
        # Update only provided fields
        update_data = data.model_dump(exclude_unset=True)
        if update_data:
            await course.update_from_dict(update_data).save()
            await course.refresh_from_db()
            logger.info("Successfully updated course", course_id=str(course_id), user_id=str(user_id))
        
        return json(format_course_response(course))
        
    except ValueError as e:
        logger.warning("Validation error updating course", error=str(e), course_id=str(course_id), user_id=str(user_id))
        return json({"error": str(e)}, status=400)
    except IntegrityError as e:
        logger.exception("Database error updating course", course_id=str(course_id), user_id=str(user_id))
        return json({"error": "Database error occurred"}, status=500)
    except Exception as e:
        logger.exception("Unexpected error updating course", course_id=str(course_id), user_id=str(user_id))
        raise

# DELETE /courses/<course_id> - Delete a course
@bp.delete("/<course_id:uuid>")
@login_required
async def delete_course(request, course_id: UUID):
    user_id = request.ctx.user_id
    try:
        course = await get_course_with_ownership(user_id, course_id)
        
        if not course:
            logger.warning("Course not found for deletion", course_id=str(course_id), user_id=str(user_id))
            return json({"error": "Course not found"}, status=404)
        
        await course.delete()
        logger.info("Successfully deleted course", course_id=str(course_id), user_id=str(user_id))
        return response.empty(status=204)
    except Exception as e:
        logger.exception("Error deleting course", course_id=str(course_id), user_id=str(user_id))
        return json({"error": "Failed to delete course"}, status=500)

# Error handlers
@bp.exception(ValueError)
async def handle_validation_error(request, exception):
    logger.warning("Validation error", error=str(exception))
    return json({"error": str(exception)}, status=400)

@bp.exception(IntegrityError)
async def handle_integrity_error(request, exception):
    logger.exception("Database integrity error")
    return json({"error": "Database error occurred"}, status=500)

@bp.exception(Exception)
async def handle_generic_error(request, exception):
    logger.exception("Unexpected error")
    return json({"error": "Internal server error"}, status=500)
