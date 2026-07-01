"""
user_model.py
-------------
Pydantic models for user profiles and preferences.
"""

from typing import Optional
from pydantic import BaseModel, Field


class UserPreferences(BaseModel):
    """Accessibility and UI preferences."""
    voice_speed: float = Field(default=1.0, ge=0.5, le=2.0, description="TTS speech speed")
    voice_language: str = "en"
    high_contrast: bool = False
    screen_reader_mode: bool = True
    verbose_responses: bool = False  # If True, agent gives more detailed answers


class UserProfile(BaseModel):
    """User's career profile used by agents for personalization."""
    user_id: str
    name: str = ""
    email: str = ""
    target_roles: list[str] = []
    preferred_locations: list[str] = ["remote"]
    skills: list[str] = []
    experience_years: int = 0
    education: str = ""
    disability_accommodations: list[str] = []  # e.g. ["screen reader", "voice input"]
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    resume_sections: dict[str, str] = {}  # section_name -> formatted text


class UserProfileUpdate(BaseModel):
    """Partial update model for user profile."""
    name: Optional[str] = None
    email: Optional[str] = None
    target_roles: Optional[list[str]] = None
    preferred_locations: Optional[list[str]] = None
    skills: Optional[list[str]] = None
    experience_years: Optional[int] = None
    education: Optional[str] = None
    disability_accommodations: Optional[list[str]] = None
    preferences: Optional[UserPreferences] = None
