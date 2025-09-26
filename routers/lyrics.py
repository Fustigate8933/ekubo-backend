"""
Lyrics router for managing lyrics and lyric lines.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from models import LyricsCreate, LyricsResponse, LyricsWithLines, LyricLineCreate, LyricLineResponse
from services.supabase_service import supabase_service

router = APIRouter()


@router.get("/", response_model=List[LyricsResponse])
async def get_lyrics(
    skip: int = Query(0, ge=0, description="Number of lyrics to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of lyrics to return"),
    synced_lyrics: Optional[str] = Query(None, description="Filter by synced lyrics content")
):
    """Get all lyrics with pagination and optional filters."""
    try:
        filters = {}
        if synced_lyrics:
            filters["synced_lyrics"] = synced_lyrics
        
        if filters:
            lyrics = await supabase_service.search("lyrics", filters, skip=skip, limit=limit)
        else:
            lyrics = await supabase_service.get_multi("lyrics", skip=skip, limit=limit)
        return lyrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch lyrics: {str(e)}")


@router.get("/{lyrics_id}", response_model=LyricsWithLines)
async def get_lyrics_with_lines(lyrics_id: int):
    """Get lyrics with all associated lines."""
    try:
        lyrics = await supabase_service.get("lyrics", lyrics_id)
        if not lyrics:
            raise HTTPException(status_code=404, detail="Lyrics not found")
        
        # Get lyric lines
        lyric_lines = await supabase_service._make_request(
            "GET", 
            f"lyric_lines?lyrics_id=eq.{lyrics_id}",
            params={"order": "id"}
        )
        lyrics["lyric_lines"] = lyric_lines
        
        return lyrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch lyrics: {str(e)}")


@router.post("/", response_model=LyricsResponse)
async def create_lyrics(lyrics_data: LyricsCreate):
    """Create new lyrics."""
    try:
        lyrics = await supabase_service.create("lyrics", lyrics_data.model_dump())
        return lyrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create lyrics: {str(e)}")


@router.put("/{lyrics_id}", response_model=LyricsResponse)
async def update_lyrics(lyrics_id: int, lyrics_data: LyricsCreate):
    """Update lyrics."""
    lyrics = await supabase_service.get("lyrics", lyrics_id)
    if not lyrics:
        raise HTTPException(status_code=404, detail="Lyrics not found")
    
    try:
        updated_lyrics = await supabase_service.update("lyrics", lyrics_id, lyrics_data.model_dump())
        return updated_lyrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update lyrics: {str(e)}")


@router.delete("/{lyrics_id}")
async def delete_lyrics(lyrics_id: int):
    """Delete lyrics."""
    lyrics = await supabase_service.get("lyrics", lyrics_id)
    if not lyrics:
        raise HTTPException(status_code=404, detail="Lyrics not found")
    
    try:
        success = await supabase_service.delete("lyrics", lyrics_id)
        if success:
            return {"message": "Lyrics deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete lyrics")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete lyrics: {str(e)}")


@router.post("/{lyrics_id}/lines", response_model=LyricLineResponse)
async def create_lyric_line(lyrics_id: int, line_data: LyricLineCreate):
    """Create a new lyric line."""
    try:
        # Verify lyrics exist
        lyrics = await supabase_service.get("lyrics", lyrics_id)
        if not lyrics:
            raise HTTPException(status_code=404, detail="Lyrics not found")
        
        # Create lyric line
        line_data_dict = line_data.model_dump()
        line_data_dict["lyrics_id"] = lyrics_id
        lyric_line = await supabase_service.create("lyric_lines", line_data_dict)
        return lyric_line
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create lyric line: {str(e)}")


@router.get("/{lyrics_id}/lines", response_model=List[LyricLineResponse])
async def get_lyric_lines(lyrics_id: int):
    """Get all lyric lines for specific lyrics."""
    try:
        # Verify lyrics exist
        lyrics = await supabase_service.get("lyrics", lyrics_id)
        if not lyrics:
            raise HTTPException(status_code=404, detail="Lyrics not found")
        
        # Get lyric lines
        lyric_lines = await supabase_service._make_request(
            "GET", 
            f"lyric_lines?lyrics_id=eq.{lyrics_id}",
            params={"order": "id"}
        )
        return lyric_lines
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch lyric lines: {str(e)}")