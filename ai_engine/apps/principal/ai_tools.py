"""
LLM tools for course management.

This module provides LangChain tools that mirror the functionality of the course management REST API.
These tools allow the LLM to interact with courses in a similar way to the HTTP endpoints.
"""

from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime
from pydantic import Field, BaseModel, field_validator
from langchain.tools import BaseTool
from loguru import logger
from tortoise.exceptions import DoesNotExist

from ai_engine.apps.course.models import Course
from ai_engine.apps.principal.course import generate_course_outline
from ai_engine.logging import log_exception
from ai_engine.apps.auth.models import User

class CourseCreateInput(BaseModel):
    """Input model for course creation."""
    name: str = Field(..., description="Name of the course")
    description: str = Field(..., description="Description of the course")

class CourseUpdateInput(BaseModel):
    """Input model for course updates."""
    name: Optional[str] = Field(None, description="New name for the course")
    description: Optional[str] = Field(None, description="New description for the course")

class BaseCourseTool(BaseTool):
    """Base class for course tools with user validation."""
    user_id: int = Field(..., description="ID of the authenticated user")

class CreateCourseTool(BaseCourseTool):
    """Tool for creating a new course."""
    name: str = Field(default="create_course", description="Name of the tool")
    description: str = Field(
        default="""Create a new course.
        Input should be a JSON string with 'name' and 'description' fields.
        Example: '{"name": "Python Basics", "description": "Learn Python programming fundamentals"}'""",
        description="Tool description"
    )
    
    async def _arun(self, input_str: str) -> str:
        """Run the tool asynchronously."""
        try:
            # Parse input
            input_data = CourseCreateInput.model_validate_json(input_str)
            
            # Get user (already validated in __init__)
            user = await User.get(id=self.user_id)
            
            # Create course
            course = await Course.create(
                name=input_data.name,
                description=input_data.description,
                owner=user
            )
            
            # Generate outline asynchronously
            #course.outline = await generate_course_outline(str(course.id))
            await course.save()
            
            return f"""Course created successfully:
            ID: {course.id}
            Name: {course.name}
            Description: {course.description}
            Created: {course.created_at.isoformat()}
            Owner: {user.username} (ID: {user.id})
            Outline: {course.outline or 'Generating...'}"""
            
        except Exception as e:
            log_exception(e, "Error creating course")
            return f"Error creating course: {str(e)}"
    
    def _run(self, input_str: str) -> str:
        """Run the tool synchronously (not supported)."""
        return "This tool only supports async operation"

class GetCourseTool(BaseCourseTool):
    """Tool for retrieving course details."""
    name: str = Field(default="get_course", description="Name of the tool")
    description: str = Field(
        default="""Get details of a course by its ID.
        Input should be a UUID string.
        Example: '123e4567-e89b-12d3-a456-426614174000'
        Note: You can only retrieve courses you own.""",
        description="Tool description"
    )
    
    async def _arun(self, course_id: str) -> str:
        """Run the tool asynchronously."""
        try:
            # Get course with owner information
            course = await Course.get(id=UUID(course_id)).prefetch_related("owner")
            
            # Check if user owns this course
            if course.owner.id != self.user_id:
                return f"Error: Access denied. You can only retrieve courses you own. This course belongs to user {course.owner.username}."
            
            return f"""Course details:
            ID: {course.id}
            Name: {course.name}
            Description: {course.description}
            Created: {course.created_at.isoformat()}
            Updated: {course.updated_at.isoformat()}
            Outline: {course.outline or 'Generating...'}
            Owner: {course.owner.username} (ID: {course.owner.id})"""
            
        except DoesNotExist:
            return f"Course with ID {course_id} not found"
        except Exception as e:
            log_exception(e, f"Error retrieving course {course_id}")
            return f"Error retrieving course: {str(e)}"
    
    def _run(self, course_id: str) -> str:
        """Run the tool synchronously (not supported)."""
        return "This tool only supports async operation"

class ListCoursesTool(BaseCourseTool):
    """Tool for listing courses with optional filtering."""
    name: str = Field(default="list_courses", description="Name of the tool")
    description: str = Field(
        default="""List courses with optional filtering.
        Input should be a JSON string with optional fields:
        - owner_id: Filter by owner ID (must be the authenticated user)
        - search: Search in name and description
        - limit: Maximum number of courses (default: 50, max: 100)
        - offset: Number of courses to skip (default: 0)
        Example: '{"search": "Python", "limit": 10}'""",
        description="Tool description"
    )
    
    async def _arun(self, input_str: str) -> str:
        """Run the tool asynchronously."""
        try:
            # Parse input
            params = CourseListParams.model_validate_json(input_str)
            
            # Build query
            query = Course.all().prefetch_related("owner")
            
            if params.owner_id:
                # Only allow filtering by own user_id
                if params.owner_id != self.user_id:
                    return f"Error: Can only filter by own user ID ({self.user_id})"
                query = query.filter(owner_id=params.owner_id)
            if params.search:
                query = query.filter(name__icontains=params.search) | query.filter(description__icontains=params.search)
            
            # Get total count
            total = await query.count()
            
            # Get paginated results
            courses = await query.offset(params.offset).limit(params.limit)
            
            # Format response
            courses_list = []
            for course in courses:
                courses_list.append(f"""
                Course:
                ID: {course.id}
                Name: {course.name}
                Description: {course.description}
                Created: {course.created_at.isoformat()}
                Updated: {course.updated_at.isoformat()}
                Outline: {course.outline or 'Generating...'}
                Owner: {course.owner.username} (ID: {course.owner.id})
                ---""")
            
            return f"""Found {total} courses (showing {len(courses_list)}):
            {''.join(courses_list)}"""
            
        except Exception as e:
            log_exception(e, "Error listing courses")
            return f"Error listing courses: {str(e)}"
    
    def _run(self, input_str: str) -> str:
        """Run the tool synchronously (not supported)."""
        return "This tool only supports async operation"

class UpdateCourseTool(BaseCourseTool):
    """Tool for updating course details."""
    name: str = Field(default="update_course", description="Name of the tool")
    description: str = Field(
        default="""Update course details.
        Input should be a JSON string with:
        - course_id: UUID of the course to update
        - name: (optional) New course name
        - description: (optional) New course description
        Example: '{"course_id": "123e4567-e89b-12d3-a456-426614174000", "name": "New Name"}'""",
        description="Tool description"
    )
    
    async def _arun(self, input_str: str) -> str:
        """Run the tool asynchronously."""
        try:
            # Parse input
            data = CourseUpdateRequest.model_validate_json(input_str)
            
            # Get course
            try:
                course = await Course.get(id=UUID(data.course_id))
            except DoesNotExist:
                return f"Course with ID {data.course_id} not found"
            
            # Verify user is owner
            if course.owner_id != self.user_id:
                return f"Error: User {self.user_id} is not the owner of this course"
            
            # Update fields if provided
            if data.name is not None:
                course.name = data.name
            if data.description is not None:
                course.description = data.description
            
            await course.save()
            
            # Regenerate outline if name or description changed
            if data.name is not None or data.description is not None:
                course.outline = await generate_course_outline(str(course.id))
                await course.save()
            
            return f"""Course updated successfully:
            ID: {course.id}
            Name: {course.name}
            Description: {course.description}
            Updated: {course.updated_at.isoformat()}
            Outline: {course.outline or 'Generating...'}"""
            
        except Exception as e:
            log_exception(e, f"Error updating course {data.course_id}")
            return f"Error updating course: {str(e)}"
    
    def _run(self, input_str: str) -> str:
        """Run the tool synchronously (not supported)."""
        return "This tool only supports async operation"

class DeleteCourseTool(BaseCourseTool):
    """Tool for deleting a course."""
    name: str = Field(default="delete_course", description="Name of the tool")
    description: str = Field(
        default="""Delete a course by its ID.
        Input should be a JSON string with:
        - course_id: UUID of the course to delete
        Example: '{"course_id": "123e4567-e89b-12d3-a456-426614174000"}'""",
        description="Tool description"
    )
    
    async def _arun(self, input_str: str) -> str:
        """Run the tool asynchronously."""
        try:
            # Parse input
            data = CourseDeleteRequest.model_validate_json(input_str)
            
            # Get course
            try:
                course = await Course.get(id=UUID(data.course_id))
            except DoesNotExist:
                return f"Course with ID {data.course_id} not found"
            
            # Verify user is owner
            if course.owner_id != self.user_id:
                return f"Error: User {self.user_id} is not the owner of this course"
            
            await course.delete()
            return f"Course {data.course_id} deleted successfully"
            
        except Exception as e:
            log_exception(e, f"Error deleting course {data.course_id}")
            return f"Error deleting course: {str(e)}"
    
    def _run(self, input_str: str) -> str:
        """Run the tool synchronously (not supported)."""
        return "This tool only supports async operation"

class RegenerateOutlineTool(BaseCourseTool):
    """Tool for regenerating a course outline."""
    name: str = Field(default="regenerate_outline", description="Name of the tool")
    description: str = Field(
        default="""Regenerate the outline for a course.
        Input should be a JSON string with:
        - course_id: UUID of the course to regenerate outline for
        Example: '{"course_id": "123e4567-e89b-12d3-a456-426614174000"}'""",
        description="Tool description"
    )
    
    async def _arun(self, input_str: str) -> str:
        """Run the tool asynchronously."""
        try:
            # Parse input
            data = CourseOutlineRequest.model_validate_json(input_str)
            
            # Get course
            try:
                course = await Course.get(id=UUID(data.course_id))
            except DoesNotExist:
                return f"Course with ID {data.course_id} not found"
            
            # Verify user is owner
            if course.owner_id != self.user_id:
                return f"Error: User {self.user_id} is not the owner of this course"
            
            # Prepare course_data dict for outline generation
            course_data = {
                "name": course.name,
                "description": course.description
            }
            # Generate new outline
            course.outline = await generate_course_outline(course_data)
            await course.save()
            
            return f"""Course outline regenerated:
            ID: {course.id}
            Name: {course.name}
            Outline: {course.outline}"""
            
        except Exception as e:
            log_exception(e, f"Error regenerating outline for course {data.course_id}")
            return f"Error regenerating outline: {str(e)}"
    
    def _run(self, input_str: str) -> str:
        """Run the tool synchronously (not supported)."""
        return "This tool only supports async operation"

# Input models for tools
class CourseListParams(BaseModel):
    """Parameters for listing courses."""
    owner_id: Optional[int] = Field(None, description="Filter by owner ID")
    search: Optional[str] = Field(None, description="Search in name and description")
    limit: int = Field(50, ge=1, le=100, description="Maximum number of courses to return")
    offset: int = Field(0, ge=0, description="Number of courses to skip")

class CourseUpdateRequest(BaseModel):
    """Request model for course updates."""
    course_id: str = Field(..., description="UUID of the course to update")
    name: Optional[str] = Field(None, description="New name for the course")
    description: Optional[str] = Field(None, description="New description for the course")

class CourseDeleteRequest(BaseModel):
    """Request model for course deletion."""
    course_id: str = Field(..., description="UUID of the course to delete")

class CourseOutlineRequest(BaseModel):
    """Request model for outline regeneration."""
    course_id: str = Field(..., description="UUID of the course to regenerate outline for")

# Export all tools
__all__ = [
    "CreateCourseTool",
    "GetCourseTool",
    "ListCoursesTool",
    "UpdateCourseTool",
    "DeleteCourseTool",
    "RegenerateOutlineTool"
]
