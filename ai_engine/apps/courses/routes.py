from sanic import Blueprint, response
from ai_engine.apps.auth import login_required
from ai_engine.apps.courses.models import Course
from ai_engine.apps.courses.utils import (
    CourseCreate, CourseUpdate, get_course_with_ownership, format_course_response
)
from sanic.response import json
from tortoise.exceptions import DoesNotExist, IntegrityError
from uuid import UUID

bp = Blueprint("courses", url_prefix="/courses")

# GET /courses/all - List all courses for the user
@bp.get("/all")
@login_required
async def get_courses(request):
    user_id = request.ctx.user_id
    courses = await Course.filter(user_id=user_id).all()
    return json([format_course_response(course) for course in courses])

# GET /courses/<course_id> - Get a specific course
@bp.get("/<course_id:uuid>")
@login_required
async def get_course(request, course_id: UUID):
    user_id = request.ctx.user_id
    course = await get_course_with_ownership(user_id, course_id)
    
    if not course:
        return json({"error": "Course not found"}, status=404)
    
    return json(format_course_response(course))

# POST /courses - Create a new course
@bp.post("")
@login_required
async def create_course(request):
    user_id = request.ctx.user_id
    
    try:
        # Validate request data
        data = CourseCreate(**request.json)
        
        # Create course
        course = await Course.create(
            user_id=user_id,
            name=data.name,
            description=data.description
        )
        
        return json(format_course_response(course), status=201)
        
    except ValueError as e:
        return json({"error": str(e)}, status=400)
    except IntegrityError as e:
        return json({"error": "Database error occurred"}, status=500)

# PUT /courses/<course_id> - Update a course
@bp.put("/<course_id:uuid>")
@login_required
async def update_course(request, course_id: UUID):
    user_id = request.ctx.user_id
    course = await get_course_with_ownership(user_id, course_id)
    
    if not course:
        return json({"error": "Course not found"}, status=404)
    
    try:
        # Validate request data
        data = CourseUpdate(**request.json)
        
        # Update only provided fields
        update_data = data.dict(exclude_unset=True)
        if update_data:
            await course.update_from_dict(update_data).save()
            # Refresh course data
            await course.refresh_from_db()
        
        return json(format_course_response(course))
        
    except ValueError as e:
        return json({"error": str(e)}, status=400)
    except IntegrityError as e:
        return json({"error": "Database error occurred"}, status=500)

# DELETE /courses/<course_id> - Delete a course
@bp.delete("/<course_id:uuid>")
@login_required
async def delete_course(request, course_id: UUID):
    user_id = request.ctx.user_id
    course = await get_course_with_ownership(user_id, course_id)
    
    if not course:
        return json({"error": "Course not found"}, status=404)
    
    try:
        await course.delete()
        return response.empty(status=204)
    except Exception as e:
        return json({"error": "Failed to delete course"}, status=500)

# Error handlers
@bp.exception(ValueError)
async def handle_validation_error(request, exception):
    return json({"error": str(exception)}, status=400)

@bp.exception(IntegrityError)
async def handle_integrity_error(request, exception):
    return json({"error": "Database error occurred"}, status=500)

@bp.exception(Exception)
async def handle_generic_error(request, exception):
    return json({"error": "Internal server error"}, status=500)
