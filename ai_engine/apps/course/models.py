"""
Database models for the course management application.

This module contains the database models for managing courses and their content.
"""

from tortoise import fields, models
from loguru import logger

class Course(models.Model):
    """
    Represents a course in the system.
    
    A course is a structured learning program created by a user (owner) that includes
    a name, description, and an outline of the course content.
    
    Fields:
        id: UUID v7 primary key
        owner: Foreign key to the User who created the course
        name: Course title (max 255 chars)
        description: Detailed course description
        created_at: Timestamp of course creation
        updated_at: Timestamp of last update
        outline: Course content outline/structure
    """
    id = fields.UUIDField(version=7, pk=True)
    owner = fields.ForeignKeyField("models.User", related_name="courses")
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    outline = fields.TextField(default="")

    class Meta:
        table = "courses"
