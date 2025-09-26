"""
Song Pydantic schemas for API.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# Pydantic schemas
class SongBase(BaseModel):
    """Base song schema."""
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    album_image_url: Optional[str] = None
    duration: Optional[int] = None
    spotify_id: Optional[str] = None


class SongCreate(SongBase):
    """Schema for creating a song."""
    title: str = Field(..., min_length=1, max_length=500)
    artist: str = Field(..., min_length=1, max_length=500)


class SongUpdate(SongBase):
    """Schema for updating a song."""
    pass


class SongResponse(SongBase):
    """Schema for song responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime


class SongInDB(SongResponse):
    """Schema for song in database."""
    pass