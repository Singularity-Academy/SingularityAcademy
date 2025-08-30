"""
RESTful API routes for course management.

This module provides endpoints for managing courses, including:
- Creating new courses
- Retrieving course details
- Updating course information
- Deleting courses
- Listing all courses
"""

from sanic import Blueprint, Request, json as sanic_json
from sanic.response import json
from sanic.exceptions import NotFound, BadRequest
from tortoise.exceptions import DoesNotExist, IntegrityError
from uuid import UUID
from typing import Optional, Dict, Any
from datetime import datetime

from ai_engine.apps.auth import login_required
from ai_engine.apps.course.models import Course
from ai_engine.logging import logger, log_exception
from ai_engine.apps.principal.course import generate_course_outline

bp = Blueprint("course", url_prefix="/course")

@bp.post("/")
@login_required
async def create_course(request: Request) -> json:
    """
    Create a new course.
    
    Request body:
    {
        "name": str,        # Required: Course name
        "description": str  # Required: Course description
    }
    
    Returns:
    {
        "id": str,          # UUID of created course
        "name": str,
        "description": str,
        "created_at": str,  # ISO format datetime
        "updated_at": str,  # ISO format datetime
        "outline": str      # Initially empty, will be generated asynchronously
    }
    """
    return json({"type": "error", "message": "Course creation is not available in the API, use the Websocket API"})

@bp.get("/<course_id:uuid>")
@login_required
async def get_course(request: Request, course_id: UUID) -> json:
    """
    Get course details by ID.
    
    Args:
        course_id: UUID of the course to retrieve
        
    Returns:
    {
        "id": str,
        "name": str,
        "description": str,
        "created_at": str,
        "updated_at": str,
        "outline": str,
        "owner": {
            "id": int,
            "username": str
        }
    }
    """
    try:
        course = await Course.get(id=course_id).prefetch_related("owner")
        return json({
            "id": str(course.id),
            "name": course.name,
            "description": course.description,
            "created_at": course.created_at.isoformat(),
            "updated_at": course.updated_at.isoformat(),
            "outline": course.outline or "Generating...",
            "owner": {
                "id": course.owner.id,
                "username": course.owner.username
            }
        })
    except DoesNotExist:
        raise NotFound(f"Course with ID {course_id} not found")
    except Exception as e:
        log_exception(e, f"Error retrieving course {course_id}")
        raise BadRequest(str(e))

@bp.get("/")
@login_required
async def list_courses(request: Request) -> json:
    """
    List all courses with optional filtering.
    
    Query parameters:
    - owner_id: Filter by owner ID
    - search: Search in name and description
    - limit: Maximum number of courses to return (default: 50)
    - offset: Number of courses to skip (default: 0)
    
    Returns:
    {
        "courses": [
            {
                "id": str,
                "name": str,
                "description": str,
                "created_at": str,
                "updated_at": str,
                "outline": str,
                "owner": {
                    "id": int,
                    "username": str
                }
            }
        ],
        "total": int,
        "limit": int,
        "offset": int
    }
    """
    try:
        # Get query parameters
        owner_id = request.args.get("owner_id")
        search = request.args.get("search", "")
        limit = min(int(request.args.get("limit", 50)), 100)  # Cap at 100
        offset = int(request.args.get("offset", 0))
        
        # Build query
        query = Course.all().prefetch_related("owner")
        
        if owner_id:
            query = query.filter(owner_id=owner_id)
        if search:
            query = query.filter(name__icontains=search) | query.filter(description__icontains=search)
            
        # Get total count
        total = await query.count()
        
        # Get paginated results
        courses = await query.offset(offset).limit(limit)
        
        return json({
            "courses": [{
                "id": str(course.id),
                "name": course.name,
                "description": course.description,
                "created_at": course.created_at.isoformat(),
                "updated_at": course.updated_at.isoformat(),
                "outline": course.outline or "Generating...",
                "owner": {
                    "id": course.owner.id,
                    "username": course.owner.username
                }
            } for course in courses],
            "total": total,
            "limit": limit,
            "offset": offset
        })
        
    except ValueError as e:
        raise BadRequest(f"Invalid query parameter: {e}")
    except Exception as e:
        log_exception(e, "Error listing courses")
        raise BadRequest(str(e))

@bp.put("/<course_id:uuid>")
@login_required
async def update_course(request: Request, course_id: UUID) -> json:
    """
    Update course details.
    
    Args:
        course_id: UUID of the course to update
        
    Request body:
    {
        "name": str,        # Optional: New course name
        "description": str  # Optional: New course description
    }
    
    Returns:
    {
        "id": str,
        "name": str,
        "description": str,
        "created_at": str,
        "updated_at": str,
        "outline": str
    }
    """
    try:
        course = await Course.get(id=course_id)
        
        # Check ownership
        if course.owner_id != request.ctx.user.id:
            raise BadRequest("You don't have permission to update this course")
            
        data = request.json
        if not data:
            raise BadRequest("Request body is required")
            
        # Update fields if provided
        if "name" in data:
            course.name = data["name"]
        if "description" in data:
            course.description = data["description"]
            
        await course.save()
        
        # Regenerate outline if name or description changed
        if "name" in data or "description" in data:
            course_data = {"name": course.name, "description": course.description}
        
        return json({
            "id": str(course.id),
            "name": course.name,
            "description": course.description,
            "created_at": course.created_at.isoformat(),
            "updated_at": course.updated_at.isoformat(),
            "outline": course.outline or "Generating..."
        })
        
    except DoesNotExist:
        raise NotFound(f"Course with ID {course_id} not found")
    except IntegrityError as e:
        logger.error(f"Database error updating course: {e}")
        raise BadRequest("A course with this name already exists")
    except Exception as e:
        log_exception(e, f"Error updating course {course_id}")
        raise BadRequest(str(e))

@bp.delete("/<course_id:uuid>")
@login_required
async def delete_course(request: Request, course_id: UUID) -> json:
    """
    Delete a course.
    
    Args:
        course_id: UUID of the course to delete
        
    Returns:
    {
        "success": true,
        "message": "Course deleted successfully"
    }
    """
    try:
        course = await Course.get(id=course_id)
        
        # Check ownership
        if course.owner_id != request.ctx.user.id:
            raise BadRequest("You don't have permission to delete this course")
            
        await course.delete()
        
        return json({
            "success": True,
            "message": "Course deleted successfully"
        })
        
    except DoesNotExist:
        raise NotFound(f"Course with ID {course_id} not found")
    except Exception as e:
        log_exception(e, f"Error deleting course {course_id}")
        raise BadRequest(str(e))

@bp.post("/<course_id:uuid>/regenerate-outline")
@login_required
async def regenerate_outline(request: Request, course_id: UUID) -> json:
    """
    Manually trigger regeneration of a course outline.
    
    Args:
        course_id: UUID of the course to regenerate outline for
        
    Returns:
    {
        "id": str,
        "name": str,
        "outline": "Generating..."
    }
    """
    try:
        course = await Course.get(id=course_id)
        
        # Check ownership
        if course.owner_id != request.ctx.user.id:
            raise BadRequest("You don't have permission to regenerate this course's outline")
            
        # Start outline generation
        course_data = {"name": course.name, "description": course.description}
        request.app.add_task(generate_course_outline(course_data))
        
        return json({
            "id": str(course.id),
            "name": course.name,
            "outline": "Generating..."
        })
        
    except DoesNotExist:
        raise NotFound(f"Course with ID {course_id} not found")
    except Exception as e:
        log_exception(e, f"Error regenerating outline for course {course_id}")
        raise BadRequest(str(e))

