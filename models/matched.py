"""
Matched song-lyrics Pydantic schemas for API.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# Pydantic schemas
class MatchedBase(BaseModel):
    """Base matched schema."""
    song_id: Optional[int] = None
    lyrics_id: Optional[int] = None
    created_by_user_id: Optional[int] = None


class MatchedCreate(MatchedBase):
    """Schema for creating a matched song-lyrics pair."""
    song_id: int = Field(..., gt=0)
    lyrics_id: int = Field(..., gt=0)
    created_by_user_id: int = Field(..., gt=0)


class MatchedUpdate(MatchedBase):
    """Schema for updating a matched song-lyrics pair."""
    pass


class MatchedResponse(MatchedBase):
    """Schema for matched song-lyrics responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime


class MatchedWithDetails(MatchedResponse):
    """Schema for matched song-lyrics with full details."""
    song: Optional["SongResponse"] = None
    lyrics: Optional["LyricsResponse"] = None
    created_by_user: Optional["UserResponse"] = None


class MatchedInDB(MatchedResponse):
    """Schema for matched song-lyrics in database."""
    pass


# Import here to avoid circular imports
from models.song import SongResponse
from models.lyrics import LyricsResponse
from models.user import UserResponse

# Update forward references
MatchedWithDetails.model_rebuild()
