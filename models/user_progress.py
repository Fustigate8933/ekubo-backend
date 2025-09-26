"""
User progress Pydantic schemas for API.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


# Pydantic schemas
class UserProgressBase(BaseModel):
    """Base user progress schema."""
    user_id: Optional[int] = None
    matched_song_id: Optional[int] = None
    practice_session_id: Optional[int] = None
    line_number: Optional[int] = None
    is_correct: Optional[bool] = None
    time_taken_ms: Optional[int] = None
    attempts_count: Optional[int] = None


class UserProgressCreate(UserProgressBase):
    """Schema for creating user progress."""
    user_id: int = Field(..., gt=0)
    matched_song_id: int = Field(..., gt=0)
    line_number: int = Field(..., ge=0)
    is_correct: bool
    time_taken_ms: int = Field(..., ge=0)


class UserProgressUpdate(UserProgressBase):
    """Schema for updating user progress."""
    pass


class UserProgressResponse(UserProgressBase):
    """Schema for user progress responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime


class UserProgressWithDetails(UserProgressResponse):
    """Schema for user progress with full details."""
    matched_song: Optional[dict] = None


class UserProgressInDB(UserProgressResponse):
    """Schema for user progress in database."""
    pass


# Practice session schemas
class PracticeSessionCreate(BaseModel):
    """Schema for creating a practice session."""
    user_id: int = Field(..., gt=0)
    matched_song_id: int = Field(..., gt=0)
    started_at: datetime = Field(default_factory=datetime.utcnow)


class PracticeSessionResponse(BaseModel):
    """Schema for practice session responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    matched_song_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    total_lines: Optional[int] = None
    correct_lines: Optional[int] = None
    accuracy_percentage: Optional[float] = None