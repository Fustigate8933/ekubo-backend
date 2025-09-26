"""
User Library Pydantic schemas for API.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# Pydantic schemas
class UserLibraryBase(BaseModel):
    """Base user library schema."""
    user_id: Optional[int] = None
    matched_song_id: Optional[int] = None


class UserLibraryCreate(UserLibraryBase):
    """Schema for creating a user library entry."""
    user_id: int = Field(..., gt=0)
    matched_song_id: int = Field(..., gt=0)


class UserLibraryUpdate(UserLibraryBase):
    """Schema for updating a user library entry."""
    pass


class UserLibraryResponse(UserLibraryBase):
    """Schema for user library responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime


class UserLibraryWithDetails(UserLibraryResponse):
    """Schema for user library with full details."""
    matched_song: Optional["MatchedWithDetails"] = None
    user: Optional["UserResponse"] = None


class UserLibraryInDB(UserLibraryResponse):
    """Schema for user library in database."""
    pass


# Import here to avoid circular imports
from models.matched import MatchedResponse, MatchedWithDetails
from models.user import UserResponse

# Update forward references
UserLibraryWithDetails.model_rebuild()
