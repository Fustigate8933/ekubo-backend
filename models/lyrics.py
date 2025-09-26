"""
Lyrics Pydantic schemas for API.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


# Pydantic schemas
class LyricLineBase(BaseModel):
    """Base lyric line schema."""
    start_time_ms: Optional[int] = None
    end_time_ms: Optional[int] = None
    text_content: Optional[str] = None


class LyricLineCreate(LyricLineBase):
    """Schema for creating a lyric line."""
    lyrics_id: int
    text_content: str = Field(..., min_length=1)


class LyricLineResponse(LyricLineBase):
    """Schema for lyric line responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    lyrics_id: int
    created_at: datetime


class LyricsBase(BaseModel):
    """Base lyrics schema."""
    synced_lyrics: Optional[str] = None


class LyricsCreate(LyricsBase):
    """Schema for creating lyrics."""
    synced_lyrics: str = Field(..., min_length=1)


class LyricsResponse(LyricsBase):
    """Schema for lyrics responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    lyric_lines: List[LyricLineResponse] = []


class LyricsInDB(LyricsResponse):
    """Schema for lyrics in database."""
    pass


class LyricsWithLines(LyricsResponse):
    """Schema for lyrics with parsed lines."""
    lyric_lines: List[LyricLineResponse] = Field(default_factory=list)
