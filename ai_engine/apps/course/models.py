"""
Database models for the course management application.

This module contains the database models for managing courses and their content.
"""

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from loguru import logger
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

class Course(models.Model):
    """
    Represents a course in the system.
    
    A course is a structured learning program that includes content, AI interactions,
    and user progress tracking.
    
    Fields:
        id: UUID v7 primary key
        owner: Foreign key to the User who created the course
        name: Course title
        description: Detailed course description
        outline: Course content outline/structure
        difficulty: Course difficulty level
        estimated_hours: Estimated time to complete
        chat_history: AI interaction history for this course
        created_at: Timestamp of course creation
        updated_at: Timestamp of last update
        last_accessed: When the course was last accessed
    """
    id = fields.UUIDField(version=7, pk=True)
    owner = fields.ForeignKeyField("models.User", related_name="courses")
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    outline = fields.JSONField(default=list)  # List of section dictionaries
    
    # Course metadata
    difficulty = fields.CharField(
        max_length=20,
        default="beginner",
        description="Course difficulty level (beginner, intermediate, advanced)"
    )
    estimated_hours = fields.IntField(
        default=10,
        description="Estimated hours to complete the course"
    )
    
    # Learning progress tracking
    chat_history = fields.JSONField(
        default=list,
        description="List of User-AI interactions during the course"
    )
    last_accessed = fields.DatetimeField(
        null=True,
        description="When the course was last accessed by any user"
    )
    
    # Timestamps
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "courses"
        indexes = (
            ("owner", "created_at"),  # For quick lookup of user's courses
            ("difficulty", "created_at"),  # For filtering by difficulty
        )

    def __str__(self):
        return f"{self.name} ({self.difficulty})"

    async def add_section(self, title: str, description: str) -> Dict[str, Any]:
        """
        Add a new section to the course outline.
        
        Args:
            title: The section title
            description: The section description
            
        Returns:
            The created section dictionary
        """
        section = {
            "section_id": f"section-{len(self.outline) + 1}",
            "title": title,
            "description": description,
            "order": len(self.outline) + 1
        }
        self.outline.append(section)
        await self.save()
        return section

    async def update_section(self, section_id: str, title: Optional[str] = None, 
                           description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Update an existing section in the course outline.
        
        Args:
            section_id: The ID of the section to update
            title: New title (optional)
            description: New description (optional)
            
        Returns:
            Updated section dictionary if found, None otherwise
        """
        for section in self.outline:
            if section["section_id"] == section_id:
                if title is not None:
                    section["title"] = title
                if description is not None:
                    section["description"] = description
                await self.save()
                return section
        return None

    async def reorder_sections(self, new_order: List[str]) -> bool:
        """
        Reorder sections in the course outline.
        
        Args:
            new_order: List of section_ids in the desired order
            
        Returns:
            True if successful, False if invalid section_ids provided
        """
        if len(new_order) != len(self.outline):
            return False
            
        # Create a mapping of section_id to section
        section_map = {section["section_id"]: section for section in self.outline}
        
        # Verify all section_ids exist
        if not all(section_id in section_map for section_id in new_order):
            return False
            
        # Create new outline with reordered sections
        new_outline = []
        for i, section_id in enumerate(new_order, 1):
            section = section_map[section_id].copy()
            section["order"] = i
            new_outline.append(section)
            
        self.outline = new_outline
        await self.save()
        return True

    async def get_section(self, section_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific section by its ID."""
        return next((section for section in self.outline if section["section_id"] == section_id), None)

    async def get_section_by_order(self, order: int) -> Optional[Dict[str, Any]]:
        """Get a section by its order number."""
        return next((section for section in self.outline if section["order"] == order), None)

    async def add_chat_message(self, role: str, content: str, message_id: Optional[str] = None):
        """
        Add a new message to the course's chat history.
        
        Args:
            role: Either 'user' or 'assistant'
            content: The message content
            message_id: Optional unique identifier for the message
        """
        message = {
            "message_id": message_id or f"{role}-{datetime.now().timestamp()}",
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        if not self.chat_history:
            self.chat_history = []
        
        self.chat_history.append(message)
        self.last_accessed = datetime.now()
        await self.save()

    async def get_recent_chat_history(self, limit: int = 10) -> List[dict]:
        """Get the most recent chat messages."""
        if not self.chat_history:
            return []
        return self.chat_history[-limit:]

    async def update_last_accessed(self):
        """Update the last accessed timestamp."""
        self.last_accessed = datetime.now()
        await self.save()

    async def get_course_stats(self) -> dict:
        """Get course statistics and metadata."""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "difficulty": self.difficulty,
            "estimated_hours": self.estimated_hours,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_accessed": self.last_accessed,
            "chat_count": len(self.chat_history) if self.chat_history else 0,
            "total_sections": len(self.outline),
            "total_chat_messages": len(self.chat_history),
            "created_at_iso": self.created_at.isoformat(),
            "updated_at_iso": self.updated_at.isoformat()
        }

# Create Pydantic models for API
Course_Pydantic = pydantic_model_creator(Course, name="Course")
CourseIn_Pydantic = pydantic_model_creator(Course, name="CourseIn", exclude_readonly=True)
