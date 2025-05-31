from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum
from datetime import datetime, date
from typing import Optional, List
from ai_engine.apps.auth.models import User

class Level(str, Enum):
    """User learning level enumeration."""
    BEGINNER = "beginner"  # 初级学习者
    INTERMEDIATE = "intermediate"  # 中级学习者
    ADVANCED = "advanced"  # 高级学习者
    EXPERT = "expert"  # 专家级学习者

    @classmethod
    def get_level_for_points(cls, points: int) -> 'Level':
        """Determine user level based on total points."""
        if points >= 5000:
            return cls.EXPERT
        elif points >= 2500:
            return cls.ADVANCED
        elif points >= 1000:
            return cls.INTERMEDIATE
        return cls.BEGINNER

class Profile(models.Model):
    """User profile model for the learning application."""
    id = fields.IntField(pk=True)
    user = fields.OneToOneField('models.User', related_name='profile', source_field='user_id')
    level = fields.CharEnumField(Level, default=Level.BEGINNER)
    streak = fields.IntField(default=0, description="Consecutive learning days")
    last_streak_update = fields.DateField(null=True)
    points = fields.IntField(default=0, description="Total learning points")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "profiles"

    def __str__(self):
        return f"{self.user.username}'s Profile"

    async def update_streak(self):
        """Update the user's learning streak."""
        today = date.today()
        
        if self.last_streak_update:
            days_since_last_update = (today - self.last_streak_update).days
            if days_since_last_update == 1:
                self.streak += 1
            elif days_since_last_update > 1:
                self.streak = 1
        else:
            self.streak = 1
        
        self.last_streak_update = today
        await self.save()

    async def add_points(self, points: int):
        """Add points and update level if needed."""
        self.points += points
        self.level = Level.get_level_for_points(self.points)
        await self.save()

    async def get_learning_stats(self) -> dict:
        """Get comprehensive learning statistics."""
        return {
            "level": self.level,
            "streak": self.streak,
            "points": self.points,
            "last_streak_update": self.last_streak_update,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

# Pydantic models for API serialization
Profile_Pydantic = pydantic_model_creator(Profile, name="Profile", exclude=("user",))
ProfileIn_Pydantic = pydantic_model_creator(Profile, name="ProfileIn", exclude_readonly=True)

# Signal handlers for automatic profile creation
@models.signals.post_save(User)
async def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile when a new user is created."""
    if created:
        await Profile.create(user=instance)
